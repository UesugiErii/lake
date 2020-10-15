# https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout

import tensorflow as tf
import numpy as np

tf.random.set_seed(0)
layer = tf.keras.layers.Dropout(.2, input_shape=(2,))
data = np.arange(10).reshape(5, 2).astype(np.float32)
print(data)

outputs = layer(data, training=True)
print(outputs)
