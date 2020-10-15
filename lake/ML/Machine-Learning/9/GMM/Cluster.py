import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np

#产生实验数据
from sklearn.datasets import make_blobs
X, y_true = make_blobs(n_samples=400, centers=4,
                       cluster_std=0.60, random_state=0)
X = X[:, ::-1] #交换列是为了方便画图


gmm = GaussianMixture(n_components=4, covariance_type='full').fit(X)
labels = gmm.predict(X)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis');
plt.show()

#由于GMM有一个隐含的概率模型，因此它也可能找到簇分配的概率结果——在Scikit-Learn中用predict_proba方法
#实现。这个方法返回一个大小为[n_samples, n_clusters]的矩阵，矩阵会给出任意属于某个簇的概率
probs = gmm.predict_proba(X)
print(probs[:5].round(3))

#输出结果
# [[0.525 0.475 0.    0.   ]
#  [0.    0.    0.    1.   ]
#  [0.    0.    0.    1.   ]
#  [1.    0.    0.    0.   ]
#  [0.    0.    0.    1.   ]]

#将每个点簇分配的概率可视化
size = 50 * probs.max(1) ** 2  #平方放大概率的差异
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', s=size);
plt.show()