# http://contrib.scikit-learn.org/metric-learn/generated/metric_learn.NCA.html

from metric_learn import NCA
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier

nca = NCA()
X, y = make_classification()
nca.fit(X, y)
knn = KNeighborsClassifier(metric=nca.get_metric())
knn.fit(X, y)
print(knn.predict(X[0: 2, :]))
print(y[0:2])
