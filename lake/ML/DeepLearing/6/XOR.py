# use neural network implement XOR classifier

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
import tensorflow.keras.optimizers as optim
import numpy as np
import os

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"


class NN(Model):
    def __init__(self):
        super(NN, self).__init__()
        self.d1 = Dense(2, activation="relu")
        self.d2 = Dense(1)

    @tf.function
    def call(self, inputs):
        x = self.d1(inputs)
        x = self.d2(x)
        return x

    def loss(model, inputs, targets):
        error = model(inputs) - targets
        return tf.reduce_mean(tf.square(error))

    def grad(model, inputs, targets):
        with tf.GradientTape() as tape:
            loss_value = NN.loss(model, inputs, targets)
        return tape.gradient(loss_value, model.trainable_weights)


x = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], dtype=np.float32)
y = np.array([[0.0], [1.0], [1.0], [0.0]], dtype=np.float32)

batch_size = 32
model = NN()
model.build((None, 2))

optimizer = optim.SGD(lr=0.02)

for i in range(10001):

    grads = model.grad(x, y)
    optimizer.apply_gradients(zip(grads, model.trainable_weights))

    if i % 2000 == 0:
        loss = model.loss(x, y)
        format_string = "epoch {}: loss {:.3f}"
        print(format_string.format(i, float(loss)))

print(model.d1.trainable_weights)
print(model.d2.trainable_weights)

# Not necessarily at the global minimum, depends on initialization

# epoch 0: loss 0.322
# epoch 2000: loss 0.000
# epoch 4000: loss 0.000
# epoch 6000: loss 0.000
# epoch 8000: loss 0.000
# epoch 10000: loss 0.000
# [<tf.Variable 'dense/kernel:0' shape=(2, 2) dtype=float32, numpy=
# array([[ 1.1348271,  0.8246266],
#        [-1.1348273, -0.8246269]], dtype=float32)>, <tf.Variable 'dense/bias:0' shape=(2,) dtype=float32, numpy=array([4.1251486e-08, 8.2462704e-01], dtype=float32)>]
# [<tf.Variable 'dense_1/kernel:0' shape=(2, 1) dtype=float32, numpy=
# array([[ 1.7623624],
#        [-1.2126517]], dtype=float32)>, <tf.Variable 'dense_1/bias:0' shape=(1,) dtype=float32, numpy=array([0.99999034], dtype=float32)>]
