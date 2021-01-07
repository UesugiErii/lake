# 等势面
# 利用查找数值实现


import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

sigma = 0.5
target_v = 0.1  # 目标等势面值
threshold = 0.01  # 控制误差需要在多少以内
search_ratio = 2  # 用来控制搜索范围
search_n = 512  # 控制搜索多少个点
n = 256  # 绘图使用多个数据点


def get_z(X: np.array, Y: np.array, input: List[Tuple]):
    # 计算与要求的势(target_v)最近的z值

    max_z = -float("inf")
    min_z = float("inf")
    for point in input:
        if point[2] < min_z:
            min_z = point[2]
        if point[2] > max_z:
            max_z = point[2]

    Z = np.zeros_like(X)
    z = np.linspace(
        min_z - search_ratio * (max_z - min_z),
        max_z + search_ratio * (max_z - min_z),
        search_n)

    z = np.linspace(
        -5,
        5,
        search_n)

    for i in range(n):
        for j in range(n):
            x = X[i][j]
            y = Y[i][j]

            # xy_error = sum([(x - point[0]) ** 2 for point in input]) + \
            #            sum([(y - point[1]) ** 2 for point in input])

            xyz_error = np.zeros(shape=(search_n,), dtype=np.float32)

            for point in input:
                xyz_error += np.e ** (
                        -1 *
                        (
                                (
                                        (z - point[2]) ** 2 + (x - point[0]) ** 2 + (y - point[1]) ** 2
                                ) ** 0.5 / sigma
                        ) ** 2
                )

            error = np.abs(xyz_error - target_v)
            min_error_index = np.argmin(error)
            print(np.min(error), np.max(error))
            # min_error = xyz_error[min_error_index]
            Z[i][j] = z[min_error_index]

    return Z


def main():
    # input_x = [0, 0.1, 0.7, 1.2, 1.9]
    # input_y = [-0.5, 1, 0, 1.1, 1.8]
    # input_z = [1, 1.5, 1, 1.3, 2]

    input_x = [0]
    input_y = [0]
    input_z = [0]

    x = np.linspace(
        min(input_x) - 0.4 * (max(input_x) - min(input_x)),
        max(input_x) + 0.4 * (max(input_x) - min(input_x)),
        n)
    y = np.linspace(
        min(input_y) - 0.4 * (max(input_y) - min(input_y)),
        max(input_y) + 0.4 * (max(input_y) - min(input_y)),
        n)

    x = np.linspace(
        -5,
        5,
        n)
    y = np.linspace(
        -5,
        5,
        n)

    X, Y = np.meshgrid(x, y)  # 关于meshgrid的解释 https://blog.csdn.net/sinat_29957455/article/details/78825945

    Z = get_z(X, Y, list(zip(input_x, input_y, input_z)))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, color='b')

    # 关闭坐标轴
    plt.xticks([])
    plt.yticks([])

    plt.show()


if __name__ == '__main__':
    main()
