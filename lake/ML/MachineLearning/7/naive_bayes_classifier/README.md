copy from [朴素贝叶斯算法原理小结](https://www.cnblogs.com/pinard/p/6069267.html), [scikit-learn 朴素贝叶斯类库使用小结](https://www.cnblogs.com/pinard/p/6074222.html)

scikit-learn中有3个朴素贝叶斯(7.3)的分类算法类

1. GaussianNB, 先验为高斯分布的朴素贝叶斯, 适合样本特征的分布大部分是连续值

2. MultinomialNB, 先验为多项式分布的朴素贝叶斯, 适合样本特征的分大部分是多元离散值

3. BernoulliNB, 先验为伯努利分布的朴素贝叶斯, 适合样本特征是二元离散值或者很稀疏的多元离散值

## GaussianNB类参数

GaussianNB类的主要参数仅有一个，即先验概率priors ，对应Y的各个类别的先验概率P(Y=Ck)。这个值默认不给出，如果不给出此时P(Y=Ck)=mk/m。其中m为训练集样本总数量，mk为输出为第k类别的训练集样本数。如果给出的话就以priors 为准。

## MultinomialNB类参数

MultinomialNB参数比GaussianNB多，但是一共也只有仅仅3个。其中，参数alpha即为上面的常数λ，如果你没有特别的需要，用默认的1即可。如果发现拟合的不好，需要调优时，可以选择稍大于1或者稍小于1的数。布尔参数fit_prior表示是否要考虑先验概率，如果是false,则所有的样本类别输出都有相同的类别先验概率。否则可以自己用第三个参数class_prior输入先验概率，或者不输入第三个参数class_prior让MultinomialNB自己从训练集样本来计算先验概率，此时的先验概率为P(Y=Ck)=mk/m。其中m为训练集样本总数量，mk为输出为第k类别的训练集样本数。总结如下：

fit_prior|class_prior|最终先验概率
:--:|:--:|:--:
false|填或者不填没有意义|P(Y=Ck)=1/k
true|不填|P(Y=Ck)=mk/m
true|填|P(Y=Ck)=class_prior

## BernoulliNB类参数

BernoulliNB一共有4个参数，其中3个参数的名字和意义和MultinomialNB完全相同。唯一增加的一个参数是binarize。这个参数主要是用来帮BernoulliNB处理二项分布的，可以是数值或者不输入。如果不输入，则BernoulliNB认为每个数据特征都已经是二元的。否则的话，小于binarize的会归为一类，大于binarize的会归为另外一类。
