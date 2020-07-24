# copy from https://www.cnblogs.com/pinard/p/6200579.html

import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs

# X为样本特征，Y为样本簇类别， 共1000个样本，每个样本2个特征，共4个簇，簇中心在[-1,-1], [0,0],[1,1], [2,2]
X, y = make_blobs(n_samples=1000, n_features=2, centers=[[-1, -1], [0, 0], [1, 1], [2, 2]],
                  cluster_std=[0.4, 0.3, 0.4, 0.3],
                  random_state=9)
plt.scatter(X[:, 0], X[:, 1], marker='o')
plt.title('train data')
plt.show()

# 不输入可选的类别数k
from sklearn.cluster import Birch

y_pred = Birch(n_clusters=None).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title('k = None')
plt.show()
from sklearn import metrics

print('---------------------------------------------------------')
print('k = None')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

# set k=4
y_pred = Birch(n_clusters=4).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.title('k = 4')
plt.show()
print('---------------------------------------------------------')
print('k = 4')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

# 调参
y_pred = Birch(n_clusters=4, threshold=0.3).fit_predict(X)
print('---------------------------------------------------------')
print('k = 4, threshold = 0.3')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

y_pred = Birch(n_clusters=4, threshold=0.1).fit_predict(X)
print('---------------------------------------------------------')
print('k = 4, threshold = 0.1')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

y_pred = Birch(n_clusters=4, threshold=0.3, branching_factor=20).fit_predict(X)
print('---------------------------------------------------------')
print('k = 4, threshold = 0.3, branching_factor = 20')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

y_pred = Birch(n_clusters=4, threshold=0.3, branching_factor=10).fit_predict(X)
print('---------------------------------------------------------')
print('k = 4, threshold = 0.3, branching_factor = 10')
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))
