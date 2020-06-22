# 全局对比度归一化(global contrast normalization, GCN)
# https://www.tensorflow.org/api_docs/python/tf/image/per_image_standardization

import tensorflow as tf

# Linearly scales each image in image to have mean 0 and variance 1.
image = tf.image.per_image_standardization(
    image
)
