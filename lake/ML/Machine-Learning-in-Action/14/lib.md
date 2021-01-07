[介绍 tensorflow 中 svd 的用法](https://tensorflow.google.cn/api_docs/python/tf/linalg/svd)

```
s, u, v = tf.linalg.svd(
        a,
        full_matrices=False,
        compute_uv=True,
    )
```

假设 a 的维度是100*20

如果 full_matrices 是 True , 那么 suv 的维度依次是 (20,), (100, 100), (20, 20)

如果 full_matrices 是 False , 那么 suv 的维度依次是 (20,) (100, 20) (20, 20)

full_matrices 默认是 False

如果 compute_uv 是 False , 表示进行奇异值分解

如果 compute_uv 是 False , 表示只计算奇异值

compute_uv 默认是 True
