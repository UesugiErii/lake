# copy from https://blog.csdn.net/FelixWang0515/article/details/94629025

import numpy as np
import matplotlib.pyplot as plt
import sklearn.svm as svm
from sklearn import datasets
from sklearn.preprocessing import StandardScaler


# generate data
def dbmoon(N=100, d=2, r=10, w=2):
    N1 = 10 * N
    w2 = w / 2
    done = True
    data = np.empty(0)
    while done:
        # generate Rectangular data
        tmp_x = 2 * (r + w2) * (np.random.random([N1, 1]) - 0.5)
        tmp_y = (r + w2) * np.random.random([N1, 1])
        tmp = np.concatenate((tmp_x, tmp_y), axis=1)
        tmp_ds = np.sqrt(tmp_x * tmp_x + tmp_y * tmp_y)
        # generate double moon data ---upper
        idx = np.logical_and(tmp_ds > (r - w2), tmp_ds < (r + w2))
        idx = (idx.nonzero())[0]

        if data.shape[0] == 0:
            data = tmp.take(idx, axis=0)
        else:
            data = np.concatenate((data, tmp.take(idx, axis=0)), axis=0)
        if data.shape[0] >= N:
            done = False
    # print (data)
    db_moon = data[0:N, :]
    # print (db_moon)
    # generate double moon data ----down
    data_t = np.empty([N, 2])
    data_t[:, 0] = data[0:N, 0] + r
    data_t[:, 1] = -data[0:N, 1] - d
    db_moon = np.concatenate((db_moon, data_t), axis=0)
    return db_moon


# 然后生成200个数据点，可分为两类，
# 其中的70个数据点作为测试数据，
# 10个作为有标签数据，
# 120个作为无标签数据，
# 数据分配代码如下
N = 100
d = -2
r = 10
w = 2
a = 0.1
num_MSE = []
num_step = []
data = []
label = []
data_tmp = dbmoon(N, d, r, w)
for i in range(N):
    data.append([data_tmp[i, 0], data_tmp[i, 1]])
    label.append(-1)
    data.append([data_tmp[i + N, 0], data_tmp[i + N, 1]])
    label.append(1)
data = np.array(data)
label = np.array(label)
# standardizing
sc = StandardScaler()
sc.fit(data)
data = sc.transform(data)
# 对生成的数据进行分配
test_d, test_c = data[:70], label[:70]
l_d, l_c = data[70:80], label[70:80]
u_d = data[80:200]  # 60
lu_d = np.concatenate((l_d, u_d))
n = len(l_d) + len(u_d)

# 接下来直接调用Sklearn中的svm创建两个支持向量机模型，
# 其中一个直接使用10个有标签的数据样本进行训练，训练完成直接对测试数据进行分类。
# 另外一个用于构建TSVM

clf1 = svm.SVC(C=1, kernel='linear')
clf1.fit(l_d, l_c)
clf0 = svm.SVC(C=1, kernel='linear')  # 这里的核函数使用 linear， 惩罚参数的值设为1，可以尝试其他值
clf0.fit(l_d, l_c)
lu_c_0 = clf0.predict(lu_d)  # clf0直接使用有标签数据训练，训练完成对测试集进行分类
u_c_new = clf1.predict(u_d)  # 这里直接使用有标签数据训练得到的SVM模型对无标签数据进行分类，将其分类结果作为无标签数据的类别
cu, cl = 0.0001, 1  # 初始化有标签数据无标签数据重要程度的折中参数
sample_weight = np.ones(n)  # 样本权重， 直接让有标签数据的权重为Cl,无标签数据的权重为Cu
# print(sample_weight)
# print()
sample_weight[len(l_c):] = cu
# print(sample_weight)
id_set = np.arange(len(u_d))
while cu < cl:
    lu_c = np.concatenate((l_c, u_c_new))  # 70
    clf1.fit(lu_d, lu_c, sample_weight=sample_weight)
    while True:
        u_c_new = clf1.predict(u_d)  # 类别预测
        u_dist = clf1.decision_function(u_d)  # 表示点到当前超平面的距离
        norm_weight = np.linalg.norm(clf1.coef_)  # 权重数组
        epsilon = 1 - u_dist * u_c_new * norm_weight
        plus_set, plus_id = epsilon[u_c_new > 0], id_set[u_c_new > 0]  # 全部正例样本
        minus_set, minus_id = epsilon[u_c_new < 0], id_set[u_c_new < 0]  # negative labelled samples
        plus_max_id, minus_max_id = plus_id[np.argmax(plus_set)], minus_id[np.argmax(minus_set)]
        a, b = epsilon[plus_max_id], epsilon[minus_max_id]
        if a > 0 and b > 0 and a + b > 2:  # 若存在一对未标记样本，其标记指派不同，并且松弛向量相加的值大于2则以为分类错误的可能性很大，需要将二者的分类标签互换，重新训练
            u_c_new[plus_max_id], u_c_new[minus_max_id] = -u_c_new[plus_max_id], -u_c_new[minus_max_id]
            lu_c = np.concatenate((l_c, u_c_new))
            clf1.fit(lu_d, lu_c, sample_weight=sample_weight)
        else:
            break
    cu = min(cu * 2, cl)  # 更新折中参数
    sample_weight[len(l_c):] = cu  # 更新权重
lu_c = np.concatenate((l_c, u_c_new))
test_c1 = clf0.predict(test_d)
test_c2 = clf1.predict(test_d)
score1 = clf0.score(test_d, test_c)  # SVM的模型精度
score2 = clf1.score(test_d, test_c)  # TSVM的模型精度

# 最后将对比结果进行可视化展示
fig = plt.figure(figsize=(16, 4))
ax = fig.add_subplot(131)
ax.scatter(test_d[:, 0], test_d[:, 1], c=test_c, marker='o', cmap=plt.cm.coolwarm)
ax.set_title('True Labels for test samples', fontsize=16)
ax1 = fig.add_subplot(132)
ax1.scatter(test_d[:, 0], test_d[:, 1], c=test_c1, marker='o', cmap=plt.cm.coolwarm)
ax1.scatter(lu_d[:, 0], lu_d[:, 1], c=lu_c_0, marker='o', s=10, cmap=plt.cm.coolwarm, alpha=.6)
ax1.set_title('SVM, score: {0:.2f}%'.format(score1 * 100), fontsize=16)
ax2 = fig.add_subplot(133)
ax2.scatter(test_d[:, 0], test_d[:, 1], c=test_c2, marker='o', cmap=plt.cm.coolwarm)
ax2.scatter(lu_d[:, 0], lu_d[:, 1], c=lu_c, marker='o', s=10, cmap=plt.cm.coolwarm, alpha=.6)
ax2.set_title('TSVM, score: {0:.2f}%'.format(score2 * 100), fontsize=16)
for a in [ax, ax1, ax2]:
    a.set_xlabel("")
    a.set_ylabel("")
plt.show()
