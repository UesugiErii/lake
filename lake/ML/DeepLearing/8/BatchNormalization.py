# https://www.tensorflow.org/api_docs/python/tf/keras/layers/BatchNormalization
# line 30,39

import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channels dimension
x_train = x_train[..., tf.newaxis].astype(np.float32)
x_test = x_test[..., tf.newaxis].astype(np.float32)

train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train, y_train)).prefetch(buffer_size=tf.data.experimental.AUTOTUNE).shuffle(10000).batch(512)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(512)


class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = Conv2D(32, 3)
        self.bn2a = tf.keras.layers.BatchNormalization()
        self.flatten = Flatten()
        self.d1 = Dense(128)
        self.bn2b = tf.keras.layers.BatchNormalization()
        self.d2 = Dense(10)
        self.bn2c = tf.keras.layers.BatchNormalization()

    def call(self, x, training=False):
        x = self.conv1(x)
        x = self.bn2a(x, training=training)
        x = tf.nn.relu(x)
        x = self.flatten(x)
        x = self.d1(x)
        x = self.bn2b(x, training=training)
        x = tf.nn.relu(x)
        x = self.d2(x)
        x = self.bn2c(x, training=training)
        x = tf.nn.softmax(x)
        return x


model = MyModel()

loss_object = tf.keras.losses.SparseCategoricalCrossentropy()

optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')


@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)

    test_loss(t_loss)
    test_accuracy(labels, predictions)


EPOCHS = 20

for epoch in range(EPOCHS):
    # 在下一个epoch开始时，重置评估指标
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    for images, labels in train_ds:
        train_step(images, labels)

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    template = 'Epoch {}, Loss: {:.4f}, Accuracy: {:.4f}, Test Loss: {:.4f}, Test Accuracy: {:.4f}'
    print(template.format(epoch + 1,
                          train_loss.result(),
                          train_accuracy.result() * 100,
                          test_loss.result(),
                          test_accuracy.result() * 100))

# Epoch 1, Loss: 0.5446, Accuracy: 93.0167, Test Loss: 2.2758, Test Accuracy: 8.9200
# Epoch 2, Loss: 0.2953, Accuracy: 98.2083, Test Loss: 2.3732, Test Accuracy: 17.1100
# Epoch 3, Loss: 0.2157, Accuracy: 99.0950, Test Loss: 1.9255, Test Accuracy: 25.4900
# Epoch 4, Loss: 0.1645, Accuracy: 99.5167, Test Loss: 0.9805, Test Accuracy: 66.9900
# Epoch 5, Loss: 0.1280, Accuracy: 99.7583, Test Loss: 0.3816, Test Accuracy: 97.2400
# Epoch 6, Loss: 0.1013, Accuracy: 99.8983, Test Loss: 0.2056, Test Accuracy: 98.2900
# Epoch 7, Loss: 0.0816, Accuracy: 99.9600, Test Loss: 0.1492, Test Accuracy: 98.6000
# Epoch 8, Loss: 0.0668, Accuracy: 99.9833, Test Loss: 0.1210, Test Accuracy: 98.6600
# Epoch 9, Loss: 0.0557, Accuracy: 99.9933, Test Loss: 0.1198, Test Accuracy: 98.7800
# Epoch 10, Loss: 0.0471, Accuracy: 100.0000, Test Loss: 0.1099, Test Accuracy: 98.8300
# Epoch 11, Loss: 0.0404, Accuracy: 100.0000, Test Loss: 0.0948, Test Accuracy: 98.8300
# Epoch 12, Loss: 0.0350, Accuracy: 100.0000, Test Loss: 0.0851, Test Accuracy: 98.8500
# Epoch 13, Loss: 0.0307, Accuracy: 100.0000, Test Loss: 0.0856, Test Accuracy: 98.8900
# Epoch 14, Loss: 0.0271, Accuracy: 100.0000, Test Loss: 0.0808, Test Accuracy: 98.8800
# Epoch 15, Loss: 0.0240, Accuracy: 100.0000, Test Loss: 0.0757, Test Accuracy: 98.9100
# Epoch 16, Loss: 0.0215, Accuracy: 100.0000, Test Loss: 0.0692, Test Accuracy: 98.9400
# Epoch 17, Loss: 0.0193, Accuracy: 100.0000, Test Loss: 0.0675, Test Accuracy: 98.9100
# Epoch 18, Loss: 0.0174, Accuracy: 100.0000, Test Loss: 0.0658, Test Accuracy: 98.9100
# Epoch 19, Loss: 0.0158, Accuracy: 100.0000, Test Loss: 0.0599, Test Accuracy: 98.9000
# Epoch 20, Loss: 0.0144, Accuracy: 100.0000, Test Loss: 0.0586, Test Accuracy: 98.8700
