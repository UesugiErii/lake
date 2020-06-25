The upper part is the original image, the lower part is the reconstructed image

Weight initialization is very important, at the beginning, I use tf.random.normal, unable to train successfully, since I forgot to set stddev, the default value is 1, it is too big.
