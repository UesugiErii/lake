# tensorflow code template on MNIST

import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Specify which card：0, 1, 2, ...
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"  # Gradually allocate memory

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
        self.conv1 = Conv2D(filters=32, kernel_size=3, strides=(1, 1), padding='valid', activation='relu')
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        self.d2 = Dense(10, activation='softmax')

    @tf.function
    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)


model = MyModel()
model.build((None, 28, 28, 1))
model.summary()

loss_object = tf.keras.losses.SparseCategoricalCrossentropy()

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')


@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(labels, predictions)


@tf.function
def test_step(images, labels):
    predictions = model(images)
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

# Epoch 1, Loss: 0.2966, Accuracy: 91.5467, Test Loss: 0.1203, Test Accuracy: 96.4600
# Epoch 2, Loss: 0.0880, Accuracy: 97.5383, Test Loss: 0.0808, Test Accuracy: 97.3500
# Epoch 3, Loss: 0.0531, Accuracy: 98.5217, Test Loss: 0.0601, Test Accuracy: 97.9700
# Epoch 4, Loss: 0.0364, Accuracy: 99.0017, Test Loss: 0.0522, Test Accuracy: 98.2300
# Epoch 5, Loss: 0.0262, Accuracy: 99.3267, Test Loss: 0.0508, Test Accuracy: 98.2500
# Epoch 6, Loss: 0.0194, Accuracy: 99.5050, Test Loss: 0.0521, Test Accuracy: 98.3100
# Epoch 7, Loss: 0.0156, Accuracy: 99.6100, Test Loss: 0.0649, Test Accuracy: 97.8700
# Epoch 8, Loss: 0.0134, Accuracy: 99.6517, Test Loss: 0.0652, Test Accuracy: 97.8500
# Epoch 9, Loss: 0.0100, Accuracy: 99.7800, Test Loss: 0.0676, Test Accuracy: 98.0500
# Epoch 10, Loss: 0.0084, Accuracy: 99.8183, Test Loss: 0.0699, Test Accuracy: 98.0600
# Epoch 11, Loss: 0.0064, Accuracy: 99.8550, Test Loss: 0.0593, Test Accuracy: 98.3100
# Epoch 12, Loss: 0.0043, Accuracy: 99.9133, Test Loss: 0.0583, Test Accuracy: 98.3400
# Epoch 13, Loss: 0.0032, Accuracy: 99.9483, Test Loss: 0.0581, Test Accuracy: 98.4300
# Epoch 14, Loss: 0.0017, Accuracy: 99.9967, Test Loss: 0.0550, Test Accuracy: 98.4500
# Epoch 15, Loss: 0.0010, Accuracy: 99.9983, Test Loss: 0.0553, Test Accuracy: 98.4800
# Epoch 16, Loss: 0.0007, Accuracy: 99.9983, Test Loss: 0.0574, Test Accuracy: 98.5600
# Epoch 17, Loss: 0.0005, Accuracy: 100.0000, Test Loss: 0.0582, Test Accuracy: 98.5900
# Epoch 18, Loss: 0.0004, Accuracy: 100.0000, Test Loss: 0.0588, Test Accuracy: 98.5600
# Epoch 19, Loss: 0.0003, Accuracy: 100.0000, Test Loss: 0.0593, Test Accuracy: 98.5400
# Epoch 20, Loss: 0.0003, Accuracy: 100.0000, Test Loss: 0.0600, Test Accuracy: 98.5200
