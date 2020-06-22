# CNN example

from tensorflow.python.keras import layers
import numpy as np

# shape is (batch_size, h, w, channel)
x = np.random.random((8, 12, 12, 3)).astype(np.float32)

c1 = layers.Conv2D(filters=64, kernel_size=(4, 4), strides=(2, 2), activation='relu')
x = c1(x)
print(x.shape)

p1 = layers.MaxPool2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None)
x = p1(x)
print(x.shape)
