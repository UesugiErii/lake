# GRU example
# https://www.tensorflow.org/api_docs/python/tf/keras/layers/GRUCell

import tensorflow as tf
from tensorflow.python.keras.layers import GRUCell
import numpy as np

input_unit_num = 512
hidden_unit_num = 256
batch_size = 16

x = np.random.random((batch_size, input_unit_num)).astype(np.float32)
h = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num)).astype(np.float32))

gru_cell = GRUCell(units=hidden_unit_num)

y, h = gru_cell(inputs=x, states=h)
y, h = gru_cell(inputs=x, states=h)
