## 变种

### 稀疏自编码器

增加 λ*sum(h) 作为惩罚项

相当与有了一个稀疏编码的先验在里面

### 去噪自编码器

输入改为被噪声损坏的x, 损失项为x和重构的平方误差

防止模型学习一个恒等函数

### 收缩自编码器

添加x对h的导数和作为惩罚项

迫使模型学习一个在x变化小时目标也没有太大变化的函数

### 随机编码器

给定x, 模型只给出h的概率发布

采样h后, 模型只给出重构x的概率发布

