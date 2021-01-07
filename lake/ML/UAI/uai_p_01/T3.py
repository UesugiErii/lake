import numpy as np
import math


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


def main():
    Ex = 0
    En = 1
    He = 0.2
    N = 1000

    xu = generate(Ex, En, He, N)

    x = xu[:, 0]

    print("骨干元素: ", int(np.sum((x > (Ex - 0.67 * En)) & (x < (Ex + 0.67 * En)))) / (N / 100), '%')
    print("基本元素: ", int(np.sum((x > (Ex - 1 * En)) & (x < (Ex + 1 * En)))) / (N / 100), '%')
    print("外围元素: ",
          int(np.sum(((x > (Ex - 2 * En)) & (x < (Ex - 1 * En))) | ((x > (Ex + 1 * En)) & (x < (Ex + 2 * En))))) / (
                      N / 100), '%')
    print("弱外围元素: ",
          int(np.sum(((x > (Ex - 3 * En)) & (x < (Ex - 2 * En))) | ((x > (Ex + 2 * En)) & (x < (Ex + 3 * En))))) / (
                      N / 100), '%')


if __name__ == "__main__":
    main()
