# use conjugate gradient method to calculate x in Ax = b
#
# this algorithm come from https://en.wikipedia.org/wiki/Conjugate_gradient_method
#
# this file give two approaches
# 1 use numpy
# 2 use tensorflow


import numpy as np
import tensorflow as tf


def conjugate_gradient_method_numpy(n, A, x, b):
    """
    numpy version
    :param n: loop time
    :param A: A
    :param x: x
    :param b: b
    :return: x
    """
    r = b - np.dot(A, x)
    p = r
    # x,r mean x ,r  , xp,rp mean x    ,r
    #           k  k               k+1   k+1
    for k in range(n):
        alpha = np.dot(np.transpose(r), r) / np.dot(np.dot(np.transpose(p), A), p)
        xp = x + np.multiply(alpha, p)
        rp = r - np.dot(np.multiply(alpha, A), p)
        # if rp is sufficiently small,then exit loop
        # if np.sum(rp) < 0.01:
        #     print("small enough")
        #     break
        beta = np.dot(np.transpose(rp), rp) / np.dot(np.transpose(r), r)
        pp = rp + np.multiply(beta, p)
        x, r, p = xp, rp, pp

    return x


def conjugate_gradient_method_tensorflow(n, A, x, b):
    """
    tensorflow version
    :param n: loop time
    :param A: A
    :param x: x
    :param b: b
    :return: x
    """
    def cond(i, n, x, r, p):
        return i < n

    def body(i, n, x, r, p):
        alpha = tf.matmul(tf.transpose(r), r) / tf.matmul(tf.matmul(tf.transpose(p), A), p)
        xp = x + alpha * p
        rp = r - tf.matmul(alpha * A, p)
        # if rp is sufficiently small,then exit loop
        beta = tf.matmul(tf.transpose(rp), rp) / tf.matmul(tf.transpose(r), r)
        pp = rp + beta * p
        return i + 1, n, xp, rp, pp

    r = b - tf.matmul(A, x)
    p = r
    i = 0
    i, n, x, r, p = tf.while_loop(cond, body, [i, n, x, r, p])
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        x = sess.run(x)
    return x


# unit test
import unittest

A = np.array([[4, 1],
              [1, 3]],dtype=np.float32)

b = np.array([[1],
              [2],
              ],dtype=np.float32)

x0 = np.array([[2],
              [1],
              ],dtype=np.float32)

x1 = np.array([[0.2356],
               [0.3384]],dtype=np.float32)

x2 = np.array([[0.0909],
               [0.6364]],dtype=np.float32)

class Test(unittest.TestCase):
    def test_numpy(self):
        assert (np.round(conjugate_gradient_method_numpy(1, A, x0, b), decimals=4)
                == x1).all()
        assert (np.round(conjugate_gradient_method_numpy(2, A, x0, b), decimals=4)
                == x2).all()

    def test_tensorflow(self):
        assert (np.round(conjugate_gradient_method_tensorflow(1, A, x0, b), decimals=4)
                == x1).all()
        assert (np.round(conjugate_gradient_method_tensorflow(2, A, x0, b), decimals=4)
                == x2).all()

if __name__ == '__main__':
    unittest.main()
