# 前面介绍了一个将GMM作为数据生成器模型的示例，目的是根据输入数据的分布创建一个新的样本集。
# 现在利用这个思路，为标准手写数字库生成新的手写数字
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import numpy as np

digits = load_digits()
# 使用PCA进行降维，让PCA算法保留投影后样本99%的方差
pca = PCA(0.99, whiten=True)
data = pca.fit_transform(digits.data)


# 画出前100个数据
def plot_digits(data):
    fig, ax = plt.subplots(10, 10, figsize=(8, 8),
                           subplot_kw=dict(xticks=[], yticks=[]))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)
    for i, axi in enumerate(ax.flat):
        im = axi.imshow(data[i].reshape(8, 8), cmap='binary')
        im.set_clim(0, 16)


plot_digits(digits.data)
plt.suptitle('train data')
plt.show()

# 对这个降维的数据使用AIC，从而得到GMM成分数量的粗略估计
n_components = np.arange(50, 210, 10)
models = [GaussianMixture(n, covariance_type='full', random_state=0)
          for n in n_components]
aics = [model.fit(data).aic(data) for model in models]
plt.plot(n_components, aics)
plt.suptitle('AIC line chart')
plt.show()

# 取使AIC最小的成分数，使用这个值生成新的数据
min_aic_index = aics.index(min(aics))*10+50
gmm = GaussianMixture(min_aic_index, covariance_type='full', random_state=0)
gmm.fit(data)
# 确认模型已经收敛
print(gmm.converged_)

# 使用GMM模型在降维的空间中画出100个新的手写数字样本，再使用PCA对象逆变换将其恢复到原始的空间
data_new, y = gmm.sample(100)
digits_new = pca.inverse_transform(data_new)
plot_digits(digits_new)
plt.suptitle('New data generated')
plt.show()
