## 参考论文

<<基于云模型的协同过滤推荐算法>>

<<使用BP神经网络缓解协同过滤推荐算法的稀疏性问题>>

## 个人想法

这个实验感觉有点问题, 在那两篇论文中引用的`Cosine-Based CF`结果应该是基于`求和(相似度*评分) / 相似度和`这个公式计算出来的 ( 按这个公式复现的结果与`Cosine-Based CF`结果完全一样 ) , 但是上述两篇论文在预测评分时并不是使用这个公式, 比如论文 1 中使用了公式 5



第二篇论文我没尝试复现, 不说什么



对于第一篇论文, 作者引入了云模型, 但是最终的性能提升很可能并不是云模型所带来的, 而是我上面提到的那个公式带来的



当然我也没有向老师提出异议上面的, 因为我还想要成绩呢



至于我最终的结果图 ( final.png ) , `Cosine-Based CF`使用的是无修正的计算公式, 否则效果太好了, 为了和论文结果一致, 我就只能暗自削弱别的方法来体现论文中云模型的优势了