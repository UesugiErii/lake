copy from https://blog.csdn.net/Haiyang_Duan/article/details/77995665

## 参数

n_clusters：一个整数，指定分类簇的数量

connectivity：一个数组或者可调用对象或者None，用于指定连接矩阵

affinity：一个字符串或者可调用对象，用于计算距离。可以为：’euclidean’，’l1’，’l2’，’mantattan’，’cosine’，’precomputed’，如果linkage=’ward’，则affinity必须为’euclidean’

memory：用于缓存输出的结果，默认为不缓存

n_components：在 v-0.18中移除

compute_full_tree：通常当训练了n_clusters后，训练过程就会停止，但是如果compute_full_tree=True，则会继续训练从而生成一颗完整的树

linkage：一个字符串，用于指定链接算法

>‘ward’：单链接single-linkage，采用d_min
>
>‘complete’：全链接complete-linkage算法，采用d_max
>
>‘average’：均连接average-linkage算法，采用d_avg

pooling_func：一个可调用对象，它的输入是一组特征的值，输出是一个数

## 属性

labels：每个样本的簇标记

n_leaves_：分层树的叶节点数量

n_components：连接图中连通分量的估计值

children：一个数组，给出了每个非节点数量

## 方法

fit(X[,y])：训练样本

fit_predict(X[,y])：训练模型并预测每个样本的簇标记
