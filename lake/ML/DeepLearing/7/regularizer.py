# https://www.tensorflow.org/api_docs/python/tf/keras/regularizers/Regularizer

import tensorflow as tf

layer = tf.keras.layers.Dense(
    5, input_dim=5,
    kernel_initializer='ones',
    kernel_regularizer=tf.keras.regularizers.l1(0.01),  # L1正则化
    activity_regularizer=tf.keras.regularizers.l2(0.01))  # L2正则化
tensor = tf.ones(shape=(5, 5)) * 2.0
out = layer(tensor)
print(out)
print(tf.math.reduce_sum(layer.losses))  # 5.25 = 5*5*0.01 + 5*0.01*(2+2+2+2+2)^2
