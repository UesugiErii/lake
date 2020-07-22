# copy from https://www.cnblogs.com/pinard/p/6074222.html
import numpy as np
from sklearn.naive_bayes import GaussianNB

X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array([1, 1, 1, 2, 2, 2])

clf = GaussianNB()
# 拟合数据
clf.fit(X, Y)
# If the amount of data in the training set is very large and cannot be loaded into memory all at once
# We can divide the training set into several equal parts,
# and call partial_fit repeatedly to learn the training set step by step
# clf.partial_fit(X, Y)
print("==Predict result by predict==")  # direct print prediction class
print(clf.predict([[-0.8, -1]]))
print("==Predict result by predict_proba==")  # print probability in each class
print(clf.predict_proba([[-0.8, -1]]))
print("==Predict result by predict_log_proba==")  # print log(probability) in each class
print(clf.predict_log_proba([[-0.8, -1]]))
