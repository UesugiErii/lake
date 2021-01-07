import numpy as np
import matplotlib.pyplot as plt


def generate(Ex, En, He, N):
    En = np.random.normal(loc=En, scale=He ** 2, size=N)
    x = np.random.normal(loc=Ex, scale=En ** 2, size=N)
    return x


def main():
    Ex = 0
    En = 1
    He = 0.3
    N = 1000
    x = generate(Ex, En, He, N)
    y = generate(Ex, En, He, N)

    plt.scatter(x, y, alpha=0.6)
    plt.show()


if __name__ == "__main__":
    main()
