# pipe usage

from multiprocessing import Process, Pipe
import numpy as np


# Pipe has size limit

def f(conn):
    conn.send(np.random.random((84, 84, 4)).astype(np.float32))


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    parent_conn.send(1)
    p.start()

    print(parent_conn.recv().shape)

    p.join()
