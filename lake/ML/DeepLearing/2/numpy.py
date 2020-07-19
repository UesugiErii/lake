import numpy as np

a = np.ones((2, 2), dtype=np.float32)
b = np.array([[1, 2], [3, 4]], dtype=np.float32)

# Transpose 转置

a_t = a.transpose()

# element-wise product 矩阵逐元素乘法
# Hadamard product

c = np.multiply(a, b)

# dot product 点积

c = np.dot(a, b)

# Identity Matrix 单位矩阵

c = np.identity(3)

# Inversion 逆

c = np.linalg.inv(a)

# pseudo-inverse 伪逆

c = np.linalg.pinv(a)

# norm 范数

c = np.linalg.norm(a, ord=1)  # L1
c = np.linalg.norm(a, ord=2)  # L2
c = np.linalg.norm(a, ord=np.inf)  # max norm

# Eigendecomposition 特征值分解
# 特征值   特征向量
eigvals, eigvectors = np.linalg.eig(a)

# Singular Value Decomposition, SVD 奇异值分解

U, D, V = np.linalg.svd(a)

# trace 迹

c = np.trace(a)

# determinant 行列式

c = np.linalg.det(a)
