# Variational Autoencoder
# VAE example on MNIST
# https://s3.amazonaws.com/img-datasets/mnist.npz

# reference
# https://zhuanlan.zhihu.com/p/34998569
# https://gist.github.com/RomanSteinberg/c4a47470ab1c06b0c45fa92d07afe2e3

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import time
import os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

t = int(time.time())  # file name of save image

mnist = tf.keras.datasets.mnist
(x_train, y_train_), (x_test, y_test_) = mnist.load_data()
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

show_flag = 1  # is show res?
save_flag = 1  # is save res?
epochs = 100


class Sampling(layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon


class Encoder(layers.Layer):
    """Maps MNIST digits to a triplet (z_mean, z_log_var, z)."""

    def __init__(self,
                 latent_dim,
                 intermediate_dim,
                 name='encoder',
                 **kwargs):
        super(Encoder, self).__init__(name=name, **kwargs)
        self.dense_proj = layers.Dense(intermediate_dim, activation='relu')
        self.dense_mean = layers.Dense(latent_dim)
        self.dense_log_var = layers.Dense(latent_dim)
        self.sampling = Sampling()

    @tf.function
    def call(self, inputs):
        x = self.dense_proj(inputs)
        z_mean = self.dense_mean(x)
        z_log_var = self.dense_log_var(x)
        z = self.sampling((z_mean, z_log_var))
        return z_mean, z_log_var, z


class Decoder(layers.Layer):
    """Converts z, the encoded digit vector, back into a readable digit."""

    def __init__(self,
                 original_dim,
                 intermediate_dim,
                 name='decoder',
                 **kwargs):
        super(Decoder, self).__init__(name=name, **kwargs)
        self.dense_proj = layers.Dense(intermediate_dim, activation='relu')
        self.dense_output = layers.Dense(original_dim, activation='sigmoid')

    @tf.function
    def call(self, inputs):
        x = self.dense_proj(inputs)
        return self.dense_output(x)


class VariationalAutoEncoder(tf.keras.Model):
    """Combines the encoder and decoder into an end-to-end model for training."""

    def __init__(self,
                 original_dim,
                 intermediate_dim,
                 latent_dim,
                 name='autoencoder',
                 **kwargs):
        super(VariationalAutoEncoder, self).__init__(name=name, **kwargs)
        self.original_dim = original_dim
        self.encoder = Encoder(latent_dim=latent_dim,
                               intermediate_dim=intermediate_dim)
        self.decoder = Decoder(original_dim, intermediate_dim=intermediate_dim)

    @tf.function
    def call(self, inputs):
        z_mean, z_log_var, z = self.encoder(inputs)
        reconstructed = self.decoder(z)

        return reconstructed, z_mean, z_log_var

    @tf.function
    def binary_crossentropy(self, t, o):
        return -(t * tf.math.log(o + 1e-7) + (1.0 - t) * tf.math.log(1.0 - o + 1e-7))

    @tf.function
    def KL_Loss(self, z_mean, z_log_var):
        return - 0.5 * tf.reduce_sum(
            z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1)

    @tf.function
    def loss(self, x_batch_train, reconstructed, z_mean, z_log_var):
        # Add KL divergence regularization loss.
        kl_loss = self.KL_Loss(z_mean, z_log_var)
        # Compute reconstruction loss
        bce_loss = tf.reduce_sum(self.binary_crossentropy(x_batch_train, reconstructed))
        return kl_loss + bce_loss


loss_metric = tf.keras.metrics.Mean()

original_dim = 784
vae = VariationalAutoEncoder(original_dim, 256, 2)

optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)

(x_train, _), _ = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(60000, 784).astype('float32') / 255

train_dataset = tf.data.Dataset.from_tensor_slices(x_train)
train_dataset = train_dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE).shuffle(buffer_size=1024).batch(256)

loss_line = {'x': [], 'y': []}

for epoch in range(epochs):
    print('Start of epoch %d' % (epoch,))

    # Iterate over the batches of the dataset.
    for step, x_batch_train in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            reconstructed, z_mean, z_log_var = vae(x_batch_train)
            loss = vae.loss(x_batch_train, reconstructed, z_mean, z_log_var)

        grads = tape.gradient(loss, vae.trainable_weights)
        optimizer.apply_gradients(zip(grads, vae.trainable_weights))

        loss_metric(loss)

        if step % 100 == 0:
            print('step %s: mean loss = %s' % (step, loss_metric.result()))

    loss_line['x'].append(epoch)
    loss_line['y'].append(loss.numpy())

import matplotlib.pyplot as plt
from scipy.stats import norm

if show_flag:
    plt.plot(loss_line['x'], loss_line['y'])

# 构建encoder，然后观察各个数字在隐空间的分布
# Use encoder observe the distribution of various numbers in the hidden space
x_test_encoded = vae.encoder(x_test)[0].numpy()
plt.figure(figsize=(6, 6))
plt.scatter(x_test_encoded[:, 0], x_test_encoded[:, 1], c=y_test_)
plt.colorbar()
if save_flag:
    plt.savefig("{}_1.png".format(t))
if show_flag:
    plt.show()

# 观察隐变量的两个维度变化是如何影响输出结果的
# Observe how the two dimensions of hidden variables affect the output
n = 15  # figure with 15x15 digits
digit_size = 28
figure = np.zeros((digit_size * n, digit_size * n))

# 用正态分布的分位数来构建隐变量对
# Use normal quantiles to construct hidden variable pairs
grid_x = norm.ppf(np.linspace(0.05, 0.95, n)).astype(np.float32)
grid_y = norm.ppf(np.linspace(0.05, 0.95, n)).astype(np.float32)

for i, yi in enumerate(grid_x):
    for j, xi in enumerate(grid_y):
        z_sample = np.array([[xi, yi]])
        x_decoded = vae.decoder(z_sample).numpy()
        digit = x_decoded[0].reshape(digit_size, digit_size)
        figure[i * digit_size: (i + 1) * digit_size,
        j * digit_size: (j + 1) * digit_size] = digit

plt.figure(figsize=(10, 10))
plt.imshow(figure, cmap='Greys_r')
if save_flag:
    plt.savefig("{}_2.png".format(t))
if show_flag:
    plt.show()
