# copy from https://www.cnblogs.com/pinard/p/6235920.html

from sklearn import datasets

# 生成500个个6维的数据集，分为5个簇
X, y = datasets.make_blobs(n_samples=500, n_features=6, centers=5, cluster_std=[0.4, 0.3, 0.4, 0.3, 0.4],
                           random_state=11)

# 默认的谱聚类
from sklearn.cluster import SpectralClustering

y_pred = SpectralClustering().fit_predict(X)
from sklearn import metrics

print("无任何参数传入时 Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))

print('对n_clusters和gamma进行调参')
for index, gamma in enumerate((0.01,0.1,1,10)):
    for index, k in enumerate((3,4,5,6)):
        y_pred = SpectralClustering(n_clusters=k, gamma=gamma).fit_predict(X)
        print("Calinski-Harabasz Score with gamma=", gamma, "n_clusters=", k,"score:", metrics.calinski_harabasz_score(X, y_pred))


print('不输入可选的n_clusters的时候，仅仅用最优的gamma为0.1时候')
y_pred = SpectralClustering(gamma=0.1).fit_predict(X)
print("Calinski-Harabasz Score", metrics.calinski_harabasz_score(X, y_pred))
# 可见n_clusters一般还是调参选择比较好。