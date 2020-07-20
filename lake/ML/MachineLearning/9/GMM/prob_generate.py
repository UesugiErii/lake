# 生成实验数据
from sklearn.datasets import make_moons
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

Xmoon, ymoon = make_moons(200, noise=.05, random_state=0)
plt.scatter(Xmoon[:, 0], Xmoon[:, 1])
plt.title('train data')
plt.show()

# 如果用GMM对数据拟合出两个成分，那么作为一个聚类模型的结果，效果将会很差
gmm2 = GaussianMixture(n_components=2, covariance_type='full', random_state=0)


def draw_ellipse(position, covariance, ax=None, **kwargs):
    """用给定的位置和协方差画一个椭圆"""
    ax = ax or plt.gca()

    # 将协方差转换为主轴
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)

    # 画出椭圆
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))


def plot_gmm(gmm, X, label=True, ax=None):
    ax = ax or plt.gca()
    labels = gmm.fit(X).predict(X)
    if label:
        ax.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis', zorder=2)
    else:
        ax.scatter(X[:, 0], X[:, 1], s=40, zorder=2)
    ax.axis('equal')

    w_factor = 0.2 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covariances_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)
    plt.show()


plt.title('fit Xmoon with two Gaussians')
plot_gmm(gmm2, Xmoon)

# 如果选用更多的成分而忽视标签，就可以找到一个更接近输入数据的拟合结果
gmm16 = GaussianMixture(n_components=16, covariance_type='full', random_state=0)
plt.title('fit Xmoon with 16 Gaussians')
plot_gmm(gmm16, Xmoon, label=False)
plt.show()

# 这里采用16个高斯曲线的混合形式不是为了找到数据的分隔的簇，而是为了对输入数据的总体分布建模。
# 通过拟合后的GMM模型可以生成新的、与输入数据类似的随即分布函数。
# GMM是一种非常方便的建模方法，可以为数据估计出任意维度的随机分布

# 生成新数据

Xnew, y_new = gmm16.sample(400)
plt.scatter(Xnew[:, 0], Xnew[:, 1])
plt.title('use GaussianMixture generate new samples')
plt.show()

# 作为一种生成模型，GMM提供了一种确定数据集最优成分数量的方法。
# 由于生成模型本身就是数据集的概率分布，因此可以利用模型来评估数据的似然估计，并利用交叉检验防止过拟合。
# Scikit-Learn的GMM评估器内置了两种纠正过拟合的标准分析方法：
# 赤池信息量准则（AIC）和贝叶斯信息准则（BIC）

n_components = np.arange(1, 21)
models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(Xmoon)
          for n in n_components]

plt.plot(n_components, [m.bic(Xmoon) for m in models], label='BIC')  # 越小越好
plt.plot(n_components, [m.aic(Xmoon) for m in models], label='AIC')  # 越小越好
plt.legend(loc='best')
plt.xlabel('n_components')
plt.title('Determine the optimal number of components in the data set')
plt.show()
