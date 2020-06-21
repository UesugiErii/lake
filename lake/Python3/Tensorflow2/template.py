# tensorflow code template

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense
import tensorflow.keras.optimizers as optim


class NN(Model):
    def __init__(self, name, num_actions):
        self.name = name
        super(NN, self).__init__()
        self.d1 = Dense(20, activation="relu")
        self.d2 = Dense(num_actions)

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


input1 = 4
output1 = 2
batch_size = 32
model = NN('test1', output1)
model.build((None, input1))
para1 = model.get_weights()
x = np.ones((batch_size, input1))
res = model.predict(x)
y = np.random.random((batch_size, output1))
assert np.shape(res) == (batch_size, output1)
loss = model.loss(x, y)
grads = model.grad(x, y)
optimizer = optim.Adam(lr=0.002)
optimizer.apply_gradients(zip(grads, model.trainable_weights))
para2 = model.get_weights()
for i in range(len(para1)):
    assert not (para1[i] == para2[i]).all()
print("test past")
