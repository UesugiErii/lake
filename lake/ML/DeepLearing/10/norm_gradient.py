# https://www.tensorflow.org/api_docs/python/tf/clip_by_global_norm
# https://www.tensorflow.org/api_docs/python/tf/clip_by_norm
# https://www.tensorflow.org/api_docs/python/tf/clip_by_value

# What is the difference between them ?

# clip_by_global_norm is very similar to clip_by_norm,
# but the input of the former is t_list(A tuple or list of mixed Tensors, IndexedSlices, or None)
# input of the latter is t(A Tensor or IndexedSlices)

# clip_by_value is not recommended
# Since the true gradient direction is no longer aligned with the gradient of the small batch

# For example, the data is divided into two batchs, one batch gradient direction is (3,0), another is (0,4)
# true gradient direction is (3,4)
# if use clip_by_value and set max is 3, then the gradient of the small batch is (3,3)

import tensorflow as tf

grads, grad_norm = tf.clip_by_global_norm(grads, 0.5)
