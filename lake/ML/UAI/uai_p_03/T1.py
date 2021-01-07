# 等势线

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

sigma = 0.5


def f(x: np.array, y: np.array, input: List[Tuple]):
    # 计算势
    n = x.shape[0]
    ret = np.zeros_like(x)
    for point in input:
        ret += np.e ** (
                -1 *
                (
                        (
                                (x - point[0]) ** 2 + (y - point[1]) ** 2
                        ) ** 0.5 / sigma
                ) ** 2
        )
    return ret / n


def main():
    input_x = [0, 0.1, 0.7, 1.2, 1.9]
    input_y = [-0.5, 1, 0, 1.1, 1.8]

    n = 256
    x = np.linspace(
        min(input_x) - 0.4 * (max(input_x) - min(input_x)),
        max(input_x) + 0.4 * (max(input_x) - min(input_x)),
        n)
    y = np.linspace(
        min(input_y) - 0.4 * (max(input_y) - min(input_y)),
        max(input_y) + 0.4 * (max(input_y) - min(input_y)),
        n)

    X, Y = np.meshgrid(x, y)

    # 等高线
    plt.contour(X, Y, f(X, Y, list(zip(input_x, input_y))), colors='black')

    # 散点
    plt.scatter(input_x, input_y, marker='o', c='b')

    # 关闭坐标轴
    plt.xticks([])
    plt.yticks([])

    plt.show()


if __name__ == '__main__':
    main()
