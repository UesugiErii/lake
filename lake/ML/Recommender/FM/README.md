## FM二阶公式

\tilde{y}(x)=w_{0}+\sum_{i=1}^{n}{w_{i}x_{i}}+\sum_{i=1}^{n}{\sum_{j=i+1}^{n}{<v_{i},v_{j}>x_{i}x_{j}}}

## 优化公式

\begin{align} &\sum_{i=1}^{n}{\sum_{j=i+1}^{n}{<v_{i},v_{j}>x_{i}x_{j}}} \\ &=\frac{1}{2}\sum_{i=1}^{n}{\sum_{j=1}^{n}{<v_{i},v_{j}>x_{i}x_{j}}}-\frac{1}{2}\sum_{i=1}^{n}{<v_{i},v_{i}>x_{i}x_{i}} \\ &=\frac{1}{2}(\sum_{i=1}^{n}{\sum_{j=1}^{n}{\sum_{f=1}^{k}{v_{i,f}v_{j,f}x_{i}x_{j}}}}-\sum_{i=1}^{n}{\sum_{f=1}^{k}{v_{i,f}v_{i,f}x_{i}x_{i}}}) \\ &=\frac{1}{2}\sum_{f=1}^{k}{((\sum_{i=1}^{n}{v_{i,f}x_{i}})(\sum_{j=1}^{n}{v_{j,f}x_{j}})-\sum_{i=1}^{n}{v_{i,f}^2x_{i}^2})} \\ &=\frac{1}{2}\sum_{f=1}^{k}{((\sum_{i=1}^{n}{v_{i,f}x_{i}})^2-\sum_{i=1}^{n}{v_{i,f}^2x_{i}^2})} \end{align}

## 高阶公式

\hat{y}(x)=w_{0}+\sum_{i=1}^{n}{w_{i}x_{i}} + \sum_{l=2}^{d}{\sum_{i_{1}=1}^{n}{...\sum_{i_{l}=i_{l-1}+1}^{n}({\prod_{j=1}^{l}x_{i_{j}})(\sum_{f=1}^{k_{l}}{\prod_{j=1}^{l}{v_{i_{j},f}^{(l)}}})}}}

## 注意点

### 1

在上面两个公式中, x_i可以理解为一个事件示性函数, 当x_i这个输入存在时则为1, 否则为0

而公式里的w_i和v_i都是x_i的对应嵌入向量

### 2

高阶公式中第l阶的值是l个嵌入向量做哈达玛乘积, 再求和

## 推荐代码

[neural_factorization_machine](https://github.com/hexiangnan/neural_factorization_machine)

## 参考文章

[FM（Factorization Machines）的理论与实践](https://zhuanlan.zhihu.com/p/50426292)