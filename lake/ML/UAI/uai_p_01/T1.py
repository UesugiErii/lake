import numpy as np
import math
import matplotlib.pyplot as plt


def generate(Ex, En, He, N):
    En = np.random.normal(loc=En, scale=He, size=N)
    En = np.abs(En)
    x = np.random.normal(loc=Ex, scale=En, size=N)
    u = math.e ** (
            -(x - Ex) ** 2
            /
            (2 * En ** 2)
    )
    return np.stack([x, u], axis=1)


def get_bound(x, Ex, En, He):
    lower_bound = math.e ** (
            -(x - Ex) ** 2
            /
            (2 * (En - 3 * He) ** 2)
    )
    upper_bound = math.e ** (
            -(x - Ex) ** 2
            /
            (2 * (En + 3 * He) ** 2)
    )
    return lower_bound, upper_bound


def main():
    Ex = 0
    En = 1
    He = 0.2
    N = 1000



    xu = generate(Ex, En, He, N)

    x = np.linspace(-np.max(xu[:, 0]), np.max(xu[:, 0]), 2000)
    lower_bound, upper_bound = get_bound(x, Ex, En, He)

    plt.scatter(xu[:, 0], xu[:, 1], alpha=0.6, c='r')
    plt.plot(x, lower_bound, c='g')
    plt.plot(x, upper_bound, c='b')

    plt.show()


if __name__ == "__main__":
    main()
