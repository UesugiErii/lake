# copy from https://blog.csdn.net/qq_42797457/article/details/100675654

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.manifold import Isomap

iris = datasets.load_iris()
X = iris.data
y = iris.target

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

for idx, neighbor in enumerate([2, 20, 100]):
    isomap = Isomap(n_components=2, n_neighbors=neighbor)
    new_X_isomap = isomap.fit_transform(X)

    ax[idx].scatter(new_X_isomap[:, 0], new_X_isomap[:, 1], c=y)
    ax[idx].set_title("Isomap (n_neighbors=%d)" % neighbor)

plt.show()

# use `isomap.transform(X)` to calc new samples
