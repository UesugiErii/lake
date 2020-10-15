# Autoencoder example on MNIST

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D
import os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channels dimension
x_train = x_train[..., tf.newaxis].astype(np.float32)
x_test = x_test[..., tf.newaxis].astype(np.float32)

batch_size = 512
train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).prefetch(buffer_size=tf.data.experimental.AUTOTUNE).shuffle(10000).batch(batch_size,
                                                                                                 drop_remainder=True)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size, drop_remainder=True)


class Encoder(layers.Layer):
    def __init__(self):
        super(Encoder, self).__init__()
        # It is not recommended to use 'valid' in conv, otherwise additional operations are required in Decoder
        self.conv1 = Conv2D(filters=16, kernel_size=3, strides=(1, 1), padding='same', activation='relu')
        self.conv2 = Conv2D(filters=32, kernel_size=3, strides=(1, 1), padding='same', activation='relu')
        self.conv3 = Conv2D(filters=32, kernel_size=3, strides=(1, 1), padding='same', activation='relu')
        self.pool = MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same')
        self.flatten = Flatten()

        # self.d1 = Dense(512, activation='relu')
        # self.d2 = Dense(256, activation='relu')

    @tf.function
    def call(self, x):
        x = self.conv1(x)  # (None, 14, 14, 16)
        x = self.pool(x)  # (None, 7, 7, 16)
        x = self.conv2(x)  # (None, 7, 7, 32)
        x = self.pool(x)  # (None, 4, 4, 32)
        x = self.conv3(x)
        x = self.pool(x)
        x = self.flatten(x)  # (None,256)

        # x = tf.reshape(x, (-1, 784))
        # x = self.d1(x)
        # x = self.d2(x)

        return x


class Decoder(layers.Layer):
    def __init__(self):
        super(Decoder, self).__init__()

        self.de_w3 = tf.Variable(tf.initializers.VarianceScaling()(shape=(4, 4, 32, 32), dtype=tf.float32),
                                 trainable=True)
        self.conv3tr = Conv2D(filters=32, kernel_size=3, strides=(1, 1), padding='same', activation='relu')
        self.de_w2 = tf.Variable(tf.initializers.VarianceScaling()(shape=(7, 7, 32, 32), dtype=tf.float32),
                                 trainable=True)

        self.conv2tr = Conv2D(filters=16, kernel_size=3, strides=(1, 1), padding='same', activation='relu')
        self.de_w1 = tf.Variable(tf.initializers.VarianceScaling()(shape=(14, 14, 16, 16), dtype=tf.float32),
                                 trainable=True)
        self.conv1tr = Conv2D(filters=1, kernel_size=3, strides=(1, 1), padding='same', activation='relu')

        # self.d1 = Dense(512, activation='relu')
        # self.d2 = Dense(784, activation='relu')

    @tf.function
    def call(self, x):  # (None,256)
        x = tf.reshape(x, (-1, 4, 4, 32))
        x = tf.nn.conv2d_transpose(x, self.de_w3, (batch_size, 7, 7, 32), strides=(2, 2), padding='SAME')
        x = self.conv3tr(x)
        x = tf.nn.conv2d_transpose(x, self.de_w2, (batch_size, 14, 14, 32), strides=(2, 2), padding='SAME')
        x = self.conv2tr(x)
        x = tf.nn.conv2d_transpose(x, self.de_w1, (batch_size, 28, 28, 16), strides=(2, 2), padding='SAME')
        x = self.conv1tr(x)

        # x = self.d1(x)
        # x = self.d2(x)
        # x = tf.reshape(x, (-1, 28, 28, 1))
        return x


class AE(Model):
    def __init__(self):
        super(AE, self).__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    @tf.function
    def call(self, x):
        # CNN
        # (1,28,28,1)
        # c1   conv1tr
        # (1, 28, 28, 16)
        # p1   de_w2
        # (1, 14, 14, 16)
        # c2   conv2tr
        # (1, 14, 14, 32)
        # p2   de_w2
        # (1, 7, 7, 32)
        # c3   conv3tr
        # (1, 7, 7, 32)
        # p3   de_w3
        # (1, 4, 4, 32)

        # MLP
        # 784->512->256->512->768

        h = self.encoder(x)
        y = self.decoder(h)
        return y


model = AE()
model.build((512, 28, 28, 1))
model.summary()


@tf.function
def loss_object(img, reimg):
    return tf.reduce_sum(tf.reduce_mean(tf.math.square(img - reimg), axis=0))


optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

train_loss = tf.keras.metrics.Mean(name='train_loss')
test_loss = tf.keras.metrics.Mean(name='test_loss')


@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        reconstruction = model(images)
        loss = loss_object(images, reconstruction)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)


@tf.function
def test_step(images, labels):
    reconstruction = model(images)
    t_loss = loss_object(images, reconstruction)
    test_loss(t_loss)


EPOCHS = 100

for epoch in range(EPOCHS):
    # At the beginning of the next epoch, reset the loss
    train_loss.reset_states()
    test_loss.reset_states()

    for images, labels in train_ds:
        train_step(images, labels)

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    template = 'Epoch {}, Loss: {:.4f}, Test Loss: {:.4f}'
    print(template.format(epoch + 1,
                          train_loss.result(),
                          test_loss.result(),
                          ))

# test show, save 10 images to see result

img = np.zeros((512, 28, 28, 1), dtype=np.float32)
n = 10
sample_index = np.random.choice(10000, size=n)
img[:n] = x_test[sample_index]

reimg = model(img)
reimg = reimg.numpy()
from matplotlib import pyplot as plt

for i in range(n):
    plt.imshow(np.concatenate([np.tile(img[i], 3), np.tile(reimg[i], 3)], axis=0))
    plt.savefig('{}.png'.format(i))
