# copy from https://blog.csdn.net/qq_42797457/article/details/100675654

import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn import datasets

iris = datasets.load_iris()  # 加载数据集
X = iris.data  # 获取特征数据集 (150, 4)
y = iris.target  # 获取标签数据集 (150,)

pca = decomposition.PCA(n_components=2)  # n_components：目标维度，需要降维成n_components个特征
pca.fit(X)
new_X = pca.transform(X)  # 生成降维后的新数据
# 也可以写成
# new_X = pca.fit_transform(X)
plt.scatter(new_X[:, 0], new_X[:, 1], c=y)
plt.show()

# use `pca.transform(x)` to calc new samples
