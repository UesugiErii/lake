import numpy as np
import math
import matplotlib.pyplot as plt


def generate(Ex, En, He, N):
    En = np.random.normal(loc=En, scale=He ** 2, size=N)
    x = np.random.normal(loc=Ex, scale=En ** 2, size=N)
    return x


def main():
    Ex = 0
    En = 1
    He = 0.00001
    N = 1000

    plt.ion()
    while He < 1000000:
        plt.clf()
        plt.title('Ex: {Ex}   En: {En}   He: {He}'.format(Ex=Ex, En=En, He=He))

        x = generate(Ex, En, He, N)
        y = generate(Ex, En, He, N)

        plt.scatter(x, y, alpha=0.6, c='r')
        plt.show()

        He *= 2
        plt.pause(0.5)


if __name__ == "__main__":
    main()
