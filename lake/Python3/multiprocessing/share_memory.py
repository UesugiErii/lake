# share memory usage

from multiprocessing import Process, Array
import scipy
import numpy as np
from ctypes import c_ubyte


def f(a):
    # a[0] = -a[0]

    # write

    print(type(a))
    # a[:] = np.resize(np.array([[1,2],[3,255]]),(4,)).astype('uint8')
    a[1:2] = np.array([255, ]).astype('uint8')
    print(sum(a))


if __name__ == '__main__':
    # Create the array
    N = int(4)
    unshared_arr = scipy.rand(N).astype('uint8')
    a = Array(c_ubyte, np.zeros((4,), dtype=np.uint8))
    print(a[:])

    # Create, start, and finish the child process
    p = Process(target=f, args=(a,))
    p.start()
    p.join()

    # Print out the changed values
    print(a[:])

    # b = np.frombuffer(a.get_obj(),dtype=np.uint8)            # same address in memory
    # b = np.array(a)                             # copy
    b = a[:]
    b[0] = 10

    print(a[:])
    print(b[:])
    print(type(b))
