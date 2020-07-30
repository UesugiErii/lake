## 协同过滤

[协同过滤和基于内容推荐有什么区别？ - 行者小猪的回答 - 知乎](https://www.zhihu.com/question/19971859/answer/82255871)

[协同过滤推荐算法总结](https://www.cnblogs.com/pinard/p/6349233.html)

## 吐槽

[原作者14.5的例子](https://github.com/wzy6642/Machine-Learning-in-Action-Python3/blob/master/SVD_Project1/SVD.py )完全就是错误的, 在svdEst中TMD求了个右奇异矩阵的转置当成压缩后的样本

另外关于overLap写的真难懂, standEst中的overLap解释如下:

比如要求0的打分, 遍历用户对其他菜的打分, 如果用户对10号菜有打分, 那么就找到其他所有对0和10号菜都有打分的用户(overLap), 基于其他用户对于0和10的打分的相似度乘以用户对10的打分 -> 得到一个值, 依次对用户所有打分的菜求和, 最后除以一个总的相似度(相当与加权平均, 相似度是权重)

## 代码解释

原始数据矩阵每行为某个用户对各个菜的打分

standEst为未压缩矩阵并基于项目(item-based)的协同过滤推荐

svdEst2为压缩行并基于项目(item-based)的协同过滤推荐

svdEst为压缩列并基于用户(user-based)的协同过滤推荐
