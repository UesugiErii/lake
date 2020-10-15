# Semi-Supervised Learning
# GaussianMixture
# EM

import numpy as np
import matplotlib.pyplot as plt


# generate data
def gen_clusters():
    c1n = 400  # cluster 1 point number
    c2n = 600  # cluster 2 point number
    c3n = 500  # cluster 3 point number

    mean1 = [0, 0]  # mean
    cov1 = [[1, -0.8], [-0.8, 1]]  # covariance
    x = np.random.multivariate_normal(mean1, cov1, c1n).astype(np.float32)

    mean2 = [-2, -2]
    cov2 = [[0.5, 0], [0, 3]]
    x = np.append(x,
                  np.random.multivariate_normal(mean2, cov2, c2n).astype(np.float32),
                  0)

    mean3 = [0.5, -2.5]
    cov3 = [[1, 0.7], [0.7, 1]]
    x = np.append(x,
                  np.random.multivariate_normal(mean3, cov3, c3n).astype(np.float32),
                  0)

    y = np.empty((c1n + c2n + c3n,), dtype=np.int32)
    y[:c1n] = 1
    y[c1n:c1n + c2n] = 2
    y[c1n + c2n:] = 3

    return x, y


def show_scatter(data):
    x, y = data
    plt.scatter(x[:, 0], x[:, 1], marker='o', c=y)
    plt.axis()
    plt.title("scatter")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


data = gen_clusters()  # data is (x, y)
show_scatter(data)

# 打乱数据
indices = np.arange(data[0].shape[0])  # 样本下标集合
np.random.shuffle(indices)  # 混洗样本下标集合
X = data[0][indices]
y = data[1][indices]


def calc_p(x, mean, cov):
    # 计算多元正态分布的概率密度
    # Calculate the probability density of a multivariate normal distribution
    k = mean.shape[0]

    cov_inv = np.linalg.inv(cov)
    cov_det = np.linalg.det(cov)

    f = 1 / (np.sqrt(np.power(2 * np.pi, k) * cov_det)) * \
        np.power(np.e, -0.5 * np.dot(
            np.dot((x - mean).transpose(), cov_inv),
            x - mean
        ))
    return f


# 共1500
# 50有标签
# 1250无标签
# 200测试
label_n = 50
unlabel_n = 1300 - label_n
m = label_n + unlabel_n
test_n = 200
labeled_x = X[:label_n]
labeled_y = y[:label_n]
unlabeled_x = X[label_n:label_n + unlabel_n]
test_x = X[label_n + unlabel_n:]
test_y = y[label_n + unlabel_n:]

# 假设由3个高斯发布混合而成
k = 3
# 样本维度
d = labeled_x.shape[1]

l = np.empty((k,), dtype=np.float32)  # 第i类有标记样本数目
for i in range(1, k + 1):
    l[i - 1] = np.sum(labeled_y == i)

# 某样本属于各高斯混合成分的概率
# 初始化为对应标记样本所占比例
alpha = np.array(l) / labeled_y.shape[0]

# 某无标记样本属于各高斯混合成分的概率
# 无标记样本同样初始化
gamma = np.tile(alpha, unlabel_n).reshape([unlabel_n, k])

u = np.empty((k, d), dtype=np.float32)  # mean
sigma = np.zeros((k, d, d), dtype=np.float32)  # covariance
labeled_sigma = np.empty((k, d, d), dtype=np.float32)  # 提前计算, 方便在式13.7中直接使用, 即式13.7的最后一项

sum_i_x = np.empty((3, 2), dtype=np.float32)  # 提前计算, 方便在式13.6中直接使用, 即式13.6的最后一项

# 用有标记样本初始化均值和协方差
for i in range(k):
    i_x = labeled_x[labeled_y == i + 1]
    sum_i_x[i] = np.sum(i_x, axis=0)
    u[i] = np.mean(i_x, axis=0)

    # [协方差矩阵](https://zh.wikipedia.org/wiki/%E5%8D%8F%E6%96%B9%E5%B7%AE%E7%9F%A9%E9%98%B5)
    for j in range(i_x.shape[0]):
        sigma[i] += np.dot((i_x[j] - u[i]).reshape((2, 1)), (i_x[j] - u[i]).reshape((1, 2))) / i_x.shape[0]

    labeled_sigma[i] = sigma[i] * i_x.shape[0]

# 不使用无标记样本时的正确率
count = 0
for j in range(test_n):
    pro_i = np.zeros((3,), dtype=np.float32)
    for i in range(k):
        pro_i[i] = calc_p(test_x[j], u[i], sigma[i]) * alpha[i]
    if np.argmax(pro_i) == test_y[j] - 1:
        count += 1
print('不使用无标记样本时的正确率')
print(count / test_n)
print('u:', u)
print('sigma:', sigma)

# 使用无标记样本时的正确率
# EM
for epoch in range(1, 201):
    # E
    for j in range(unlabel_n):
        x = unlabeled_x[j]
        gamma_j = np.empty((k,))
        for i in range(k):
            gamma_j[i] = calc_p(x, u[i], sigma[i]) * alpha[i]  # 式13.6分母各项
        sum_gamma_j = np.sum(gamma_j)
        gamma_j /= sum_gamma_j
        gamma[j] = gamma_j

    # M
    for i in range(k):
        alpha[i] = (np.sum(gamma[:, i]) + l[i]) / m

        unlabel_sigma = np.zeros((d, d), dtype=np.float32)  # 式13.7括号里第一项
        for j in range(unlabel_n):
            x_j = unlabeled_x[j]
            unlabel_sigma += gamma[j][i] * np.dot(
                (x_j - u[i]).reshape((2, 1)), (x_j - u[i]).reshape((1, 2))
            )

        sigma[i] = (
                           unlabel_sigma + labeled_sigma[i]
                   ) / (
                           alpha[i] * m
                   )
        u[i] = (
                       np.sum(np.repeat(gamma[:, i], d).reshape(-1, d) * unlabeled_x, axis=0) + sum_i_x[i]
               ) / (
                       alpha[i] * m
               )

    # 每隔一段时间计算一次正确率
    count = 0
    for j in range(test_n):
        pro_i = np.zeros((3,), dtype=np.float32)
        for i in range(k):
            pro_i[i] = calc_p(test_x[j], u[i], sigma[i]) * alpha[i]
        if np.argmax(pro_i) == test_y[j] - 1:
            count += 1
    if epoch % 50 == 0:
        print('epoch: ', epoch)
        print(count / test_n)
        print('u:', u)
        print('sigma:', sigma)

print("虽然正确率没有大幅提高(有时甚至下降), 但是可以通过观察均值和协方差发现无标记样本的确起到了作用")
