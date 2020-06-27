# predictive sparse decomposition(PSD)
# 预测稀疏分解

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

x_train.resize((x_train.shape[0], 784))
x_test.resize((x_test.shape[0], 784))

batch_size = 128
train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).prefetch(buffer_size=tf.data.experimental.AUTOTUNE).shuffle(10000).batch(batch_size,
                                                                                                 drop_remainder=True)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(batch_size, drop_remainder=True)


class Encoder(Model):
    def __init__(self):
        super(Encoder, self).__init__()
        self.d1 = Dense(256, activation='relu')
        self.d2 = Dense(256, activation='relu')

    @tf.function
    def call(self, x):
        x = self.d1(x)
        h = self.d2(x)
        return h


encoder = Encoder()


class Decoder(Model):
    def __init__(self):
        super(Decoder, self).__init__()
        self.d1 = Dense(784, activation='relu')

    @tf.function
    def call(self, h):
        rex = self.d1(h)
        return rex


decoder = Decoder()


@tf.function
def loss_object(x, h, F, rex):
    # x is origin image
    # h is hidden state
    # F is encoder(x)
    # rex is decoder(h)
    loss1 = tf.sqrt(tf.nn.l2_loss(tf.subtract(x, rex)))
    loss2 = tf.reduce_sum(tf.abs(h), axis=-1)
    loss3 = tf.sqrt(tf.nn.l2_loss(tf.subtract(h, F)))
    loss = loss1 + 0.5 * loss2 + 1 * loss3
    return tf.reduce_mean(loss)


h = tf.Variable(tf.random.normal([batch_size, 256], stddev=0.01), trainable=True)

optimizer1 = tf.keras.optimizers.Adam(learning_rate=0.001)
optimizer2 = tf.keras.optimizers.Adam(learning_rate=0.001)

train_loss = tf.keras.metrics.Mean(name='train_loss')
test_loss = tf.keras.metrics.Mean(name='test_loss')


@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        rex = decoder(h)
        F = encoder(images)
        loss = loss_object(images, h, F, rex)
    gradients = tape.gradient(loss, encoder.trainable_variables + decoder.trainable_weights)
    optimizer1.apply_gradients(zip(gradients, encoder.trainable_variables + decoder.trainable_weights))
    train_loss(loss)


@tf.function
def test_step(images, labels):
    rex = decoder(h)
    F = encoder(images)
    t_loss = loss_object(images, h, F, rex)
    test_loss(t_loss)


for epoch in range(10):

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

img = np.zeros((batch_size, 784), dtype=np.float32)
n = 5
sample_index = np.random.choice(10000, size=n)
img[:n] = x_test[sample_index]

reimg = decoder(encoder(img))
reimg = reimg.numpy()
from matplotlib import pyplot as plt

for i in range(n):
    img.resize((512, 28, 28, 1))
    reimg.resize((512, 28, 28, 1))
    plt.imshow(np.concatenate([np.tile(img[i], 3), np.tile(reimg[i], 3)], axis=0))
    plt.savefig('{}.png'.format(i))
