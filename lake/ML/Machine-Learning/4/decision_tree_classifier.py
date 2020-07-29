# copy from https://www.cnblogs.com/pinard/p/6056319.html

# Environment setup
# 1. apt install graphviz
# 2. pip3 install graphviz
# 3. pip3 install pydotplus

from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=iris.feature_names,
                                class_names=iris.target_names,
                                filled=True, rounded=True,
                                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png("iris.png")
