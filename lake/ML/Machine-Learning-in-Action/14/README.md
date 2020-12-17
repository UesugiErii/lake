## SVD分解

[奇异值分解(SVD)原理与在降维中的应用](https://www.cnblogs.com/pinard/p/6251584.html)

`假设A(m*n)=U(m*k)Σ(k*k)VT(k*n), 行压缩：A'(k*n)=UT(k*m)A(m*n), 列压缩:A'(m*k)=A(m*n)V(n*k)`

## 代码注意点

在三个目录代码中, 降维直接使用了`*`来进行运算, 这是因为操作的对象是`numpy.matrix`, 此时的`*`等同于在`numpy.ndarray`上的`np.dot`