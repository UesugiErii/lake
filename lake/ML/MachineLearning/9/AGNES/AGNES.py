# modified from https://blog.csdn.net/Haiyang_Duan/article/details/77995665

from sklearn import cluster
from sklearn.metrics import adjusted_rand_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

"""
    产生数据
"""


def create_data(centers, num=100, std=0.7):
    X, labels_true = make_blobs(n_samples=num, centers=centers, cluster_std=std)
    return X, labels_true


"""
    数据作图
"""


def plot_data(*data):
    X, labels_true = data
    labels = np.unique(labels_true)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    colors = 'rgbycm'
    for i, label in enumerate(labels):
        position = labels_true == label
        ax.scatter(X[position, 0], X[position, 1], label="cluster %d" % label),
        color = colors[i % len(colors)]

    ax.legend(loc="best", framealpha=0.5)
    ax.set_xlabel("X[0]")
    ax.set_ylabel("Y[1]")
    ax.set_title("data")
    plt.show()


"""
    测试函数
"""


def test_AgglomerativeClustering(*data):
    X, labels_true = data
    clst = cluster.AgglomerativeClustering(n_clusters=4)
    predicted_labels = clst.fit_predict(X)
    print("ARI:%s" % adjusted_rand_score(labels_true, predicted_labels))  # 越大越好
    return predicted_labels


"""
    考察簇的数量对于聚类效果的影响
"""


def test_AgglomerativeClustering_nclusters(*data):
    X, labels_true = data
    nums = range(1, 50)
    ARIS = []
    for num in nums:
        clst = cluster.AgglomerativeClustering(n_clusters=num)
        predicted_lables = clst.fit_predict(X)
        ARIS.append(adjusted_rand_score(labels_true, predicted_lables))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(nums, ARIS, marker="+")
    ax.set_xlabel("n_clusters")
    ax.set_ylabel("ARI")
    fig.suptitle("AgglomerativeClustering")
    plt.show()


"""
    考察链接方式对聚类结果的影响
"""


def test_agglomerativeClustering_linkage(*data):
    X, labels_true = data
    nums = range(1, 50)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    linkages = ['ward', 'complete', 'average']
    markers = "+o*"
    for i, linkage in enumerate(linkages):
        ARIs = []
        for num in nums:
            clst = cluster.AgglomerativeClustering(n_clusters=num, linkage=linkage)
            predicted_labels = clst.fit_predict(X)
            ARIs.append(adjusted_rand_score(labels_true, predicted_labels))
        ax.plot(nums, ARIs, marker=markers[i], label="linkage:%s" % linkage)

    ax.set_xlabel("n_clusters")
    ax.set_ylabel("ARI")
    ax.legend(loc="best")
    fig.suptitle("AgglomerativeClustering")
    plt.show()


centers = [[1, 1], [2, 2], [1, 2], [10, 20]]
X, labels_true = create_data(centers, 1000, 0.5)
predicted_labels = test_AgglomerativeClustering(X, labels_true)
plot_data(X, labels_true)
plot_data(X, predicted_labels)
test_AgglomerativeClustering_nclusters(X, labels_true)
test_agglomerativeClustering_linkage(X, labels_true)
