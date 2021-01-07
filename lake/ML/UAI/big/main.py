import numpy as np
import tensorflow as tf
from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten, LSTMCell
import tensorflow.keras.optimizers as optim
import matplotlib.pyplot as plt

batch_size = 1024
hidden_unit_num = 256
N = 100
learning_rate = 0.0001


class RNN(Model):
    def __init__(self):
        super(RNN, self).__init__()
        self.optimizer = optim.Adam(learning_rate=learning_rate)
        self.lstm_cell = LSTMCell(units=hidden_unit_num)
        self.d1 = Dense(3)

    @tf.function
    def call(self, x, h, c):
        # x is inputs
        for i in range(N):
            out, hc = self.lstm_cell(inputs=x[:, i, :], states=(h, c))
        y = self.d1(out)
        return y

    @tf.function
    def loss(self, inputs, target):
        init_h = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32))
        init_c = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32))
        y = self.call(inputs, init_h, init_c)
        return tf.math.reduce_sum((y - target) ** 2) / batch_size

    @tf.function
    def train(self, inputs, target):
        with tf.GradientTape() as tape:
            loss_value = self.loss(inputs, target)

        grads = tape.gradient(loss_value, self.trainable_weights)
        grads, grad_norm = tf.clip_by_global_norm(grads, 0.5)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        return loss_value

    @tf.function
    def predict(self, inputs):
        init_h = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32))
        init_c = tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32))
        y = self.call(inputs, init_h, init_c)
        return y


def generate(Ex, En, He):
    # ret = np.empty((batch_size, N, 2))
    ret = np.empty((batch_size, N, 1))
    for i in range(batch_size):
        En_ = np.random.normal(loc=En[i], scale=He[i], size=N)
        En_ = np.abs(En_)
        x = np.random.normal(loc=Ex[i], scale=En_, size=N)
        # u = np.e ** (
        #         -(x - Ex[i]) ** 2
        #         /
        #         (2 * En_ ** 2)
        # )
        ret[i, :, 0] = x
        # ret[i, :, 1] = u
    return ret.astype(np.float32)


def generate_para():
    return np.stack([
        np.random.uniform(0, 0, batch_size),
        np.random.uniform(0, 5, batch_size),
        np.random.uniform(0, 20, batch_size)
    ], axis=1).astype(np.float32)


def generate_big_para():
    return np.stack([
        np.random.uniform(0, 0, batch_size),
        np.random.uniform(0, 50, batch_size),
        np.random.uniform(0, 200, batch_size),
    ], axis=1).astype(np.float32)


def main():
    model = RNN()
    model(
        # np.random.random((batch_size, 1000, 2)).astype(np.float32),
        np.random.random((batch_size, 1000, 1)).astype(np.float32),
        tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32)),
        tf.convert_to_tensor(np.zeros((batch_size, hidden_unit_num), dtype=np.float32))
    )
    model.summary()

    plt_data_x = []
    plt_data_y = []

    # train
    for i in range(1, 4001):
        para = generate_para()

        data = generate(para[:, 0], para[:, 1], para[:, 2])

        loss = model.train(data, para)

        plt_data_x.append(i)
        plt_data_y.append(loss)

        if i % 100 == 0:
            print(i, loss)

    plt.plot(plt_data_x, plt_data_y, 'r--', label='type1')
    plt.savefig("result2.png")

    # test
    # 在训练数据分布上进行测试
    print('=' * 40)
    test_time = 10
    sum_ = np.zeros((3,), dtype=np.float32)
    for i in range(test_time):
        para = generate_para()
        data = generate(para[:, 0], para[:, 1], para[:, 2])
        y = model.predict(data).numpy()
        sum_ += np.mean(np.abs(y - para), axis=0)
    print(sum_ / test_time)

    # big number test
    # 在非训练数据分布上进行测试
    print('=' * 40)
    test_time = 10
    sum_ = np.zeros((3,), dtype=np.float32)
    for i in range(test_time):
        para = generate_big_para()
        data = generate(para[:, 0], para[:, 1], para[:, 2])
        y = model.predict(data).numpy()
        sum_ += np.mean(np.abs(y - para), axis=0)
    print(sum_ / test_time)

    model.save_weights('model_weight')

    Ex = 0
    En = 50
    He = 200
    x = np.empty((batch_size, N, 1), dtype=np.float32)
    for i in range(1000):
        En_ = np.random.normal(loc=En, scale=He)
        x[:, i, 0] = np.random.normal(loc=Ex, scale=np.abs(En_))

    print(model.predict(x).numpy())

    return 0


if __name__ == '__main__':
    main()
