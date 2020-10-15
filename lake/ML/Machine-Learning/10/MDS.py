# copy from https://blog.csdn.net/qq_42797457/article/details/100675654

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.manifold import MDS
import numpy as np

iris = datasets.load_iris()
X = iris.data
y = iris.target

mds = MDS(n_components=2, metric=True)
new_X_mds = mds.fit_transform(X)
plt.scatter(new_X_mds[:, 0], new_X_mds[:, 1], c=y)
plt.show()



X_pinv = np.linalg.pinv(X.transpose())
Z = new_X_mds
W_tra = np.dot(Z.transpose(), X_pinv)  # formula 10.13

# use W_tra to calc new samples
