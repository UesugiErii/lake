word2vec-Tensorflow2.ipynb is copied from https://github.com/TrickyGo/Dive-into-DL-TensorFlow2.0

---

[word2vec-Tensorflow2.ipynb](./word2vec-Tensorflow2.ipynb) 是直接基于word2vec的原理进行编写的代码

[官方的 tensorflow Word embeddings](https://www.tensorflow.org/tutorials/text/word_embeddings) 是连同整个模型一起训练的

---

[word2vec原理(一) CBOW与Skip-Gram模型基础](https://www.cnblogs.com/pinard/p/7160330.html)

[word2vec原理(二) 基于Hierarchical Softmax的模型](https://www.cnblogs.com/pinard/p/7243513.html)

[word2vec原理(三) 基于Negative Sampling的模型](https://www.cnblogs.com/pinard/p/7249903.html)

### 为什么 v 和 u 不等价

[参考链接](https://discuss.gluon.ai/t/topic/4180/6)

以skipgram为例，考虑window_size=1，给定序列abcd

我们需要最大化P(b|a)P(a|b)P(c|b)P(b|c)P(d|c)P(c|d)

你会发现上面有三对相互生成。

例如下面这对

$P(b|a) P(a|b) =  \frac{ \exp(\mathbf{u}_b^\top \mathbf{v}_a)}{ \sum_i \exp(\mathbf{u}_i^\top \mathbf{v}_a)} \frac{ \exp(\mathbf{u}_a^\top \mathbf{v}_b)}{ \sum_i \exp(\mathbf{u}_i^\top \mathbf{v}_b)}$

u和v在分子等价（uv互换不影响全概率的分子大小），但分母上稍有差别。
