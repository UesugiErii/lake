# LSTM example
# https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTMCell

import tensorflow as tf
from tensorflow.python.keras.layers import LSTMCell
import numpy as np

input_unit_num = 512
hidden_unit_num = 256
batch_size = 16

x = np.random.random((batch_size, input_unit_num)).astype(np.float32)
h = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num)).astype(np.float32))
c = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num)).astype(np.float32))
hc = [h, c]

lstm_cell = LSTMCell(units=hidden_unit_num)

y, hc = lstm_cell(inputs=x, states=hc)  # hc is [h, c]
y, hc = lstm_cell(inputs=x, states=hc)
