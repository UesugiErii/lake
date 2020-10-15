遵循CC 4.0 BY-SA版权协议转载来自 [https://blog.csdn.net/jasonzhoujx/article/details/81947663](https://blog.csdn.net/jasonzhoujx/article/details/81947663)

## k-means算法的缺陷

在实际聚类的过程中，两个簇往往会存在重合部分。k-means算法对于重合部分的点被分配到哪个簇缺乏一个评估方案，k-means模型本身也没有度量簇的分配概率或不确定性的方法。

理解k-means模型的一个方法是，它在每个簇的中心放置了一个圆圈（在更高维空间是一个超空间），圆圈半径根据最远的点和簇中心点的距离算出。这个半径作为训练集分配的硬切断，即在这个圆圈之外的任何点都不是该簇的成员。而且，k-means要求这些簇的模型必须是圆形：k-means算法没有内置方法来实现椭圆形的簇。这就使得某些情况下k-means模型拟合出来的簇（圆形）与实际数据分布（可能是椭圆）差别很大，导致多个圆形的簇混在一起，相互重叠。

总的来说，k-means存在两个缺点——类的形状缺少灵活性、缺少簇分配的概率——使得它对许多数据集（特别是低维数据集）的拟合效果不尽如人意。

## 高斯混合聚类(Cluster.py)

GMM模型中的超参数convariance_type控制这每个簇的形状自由度

它的默认设置是convariance_type=’diag’,意思是簇在每个维度的尺寸都可以单独设置，但椭圆边界的主轴要与坐标轴平行。

covariance_type=’spherical’时模型通过约束簇的形状，让所有维度相等。这样得到的聚类结果和k-means聚类的特征是相似的，虽然两者并不完全相同。

covariance_type=’full’时，该模型允许每个簇在任意方向上用椭圆建模。

如果要用斜椭圆拟合, 可用

`GaussianMixture(n_components=4, covariance_type='full')`

## 将GMM用作密度估计和生成数据(prob_generate.py)

虽然GMM通常被归类为聚类算法，但他本质上是一个密度估计算法；也就是说，从技术的角度考虑，一个GMM拟合的结果并不是一个聚类模型，而是描述数据分布的生成概率模型。