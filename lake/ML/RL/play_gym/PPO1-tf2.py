import gym
import numpy as np
import tensorflow as tf
from tensorflow.python.ops.parallel_for import jacobian
from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
import tensorflow.keras.optimizers as optim


beta = 0.01
delta = 0.001

class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = Dense(20, activation="relu")
        self.d2 = Dense(1)  # C
        self.d3 = Dense(2, activation='softmax')  # A

    @tf.function
    def call(self, inputs):
        x = inputs
        x = self.d1(x)
        a = self.d3(x)
        c = self.d2(x)
        return a, c

    def a_loss(self, inputs, action_index, old_ap, adv):
        adv = tf.stop_gradient(adv)
        old_ap = tf.stop_gradient(old_ap)

        batch_size = len(inputs)
        all_act_prob = self.call(np.stack(inputs))[0]  # (128,4)
        batch_index = tf.expand_dims(tf.range(0, batch_size, dtype=tf.int32), 1)
        action_index = tf.concat([batch_index, tf.expand_dims(action_index, 1)], 1)
        selected_prob = tf.gather_nd(all_act_prob, action_index)

        L = tf.reduce_sum(
            tf.math.log(selected_prob + 1e-6) * adv
        )

        H = -tf.reduce_sum(all_act_prob[:, 0] * tf.math.log(all_act_prob[:, 0] + 1e-6) +
                           all_act_prob[:, 1] * tf.math.log(all_act_prob[:, 1] + 1e-6)
                           )



        DKL = tf.reduce_sum(
            tf.multiply(all_act_prob,
                        tf.math.log(
                            tf.divide(
                                all_act_prob,
                                old_ap
                            )
                        ))
        )

        # return -(L - beta*DKL) / batch_size , DKL
        return -(L + 0.01 * H - beta*DKL) / batch_size , DKL

    def c_loss(self, inputs, targets):
        error = self.call(inputs)[1][:, 0] - targets
        assert error.shape == (len(inputs),)
        L = tf.reduce_mean(tf.square(error))

        return L

    def a_grad(self, ob, a, old_ap, adv):
        with tf.GradientTape() as tape:
            loss_value,DKL = self.a_loss(ob, a, old_ap, adv)
        return tape.gradient(loss_value, self.trainable_weights),DKL

    def c_grad(self, obs, real_v):
        with tf.GradientTape() as tape:
            loss_value = self.c_loss(np.stack(obs), real_v)
        return tape.gradient(loss_value, self.trainable_weights)


class ProximalPolicyOptimization():
    def __init__(
            self
    ):
        self.lr = 0.1
        self.gamma = 0.99
        self.delta = 0.001
        self.ob = []
        self.a = []
        self.ap = []
        self.r = []
        self.v = []
        self.optimizer = optim.RMSprop(lr=0.01)
        self.model = MyModel()

    def choose_action(self, s):
        prob_weights, v = self.model(s[np.newaxis, :])

        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights[0])

        self.v.append(v)
        return action, prob_weights

    def learn(self):
        global beta
        global delta
        real_v = self._discount_and_norm_rewards(self.r)
        adv = real_v - np.reshape(self.v, real_v.shape)

        c_grads = self.model.c_grad(self.ob, real_v)
        a_grads,DKL = self.model.a_grad(self.ob, self.a, self.ap, adv)

        if DKL >= 1.5*delta:
            beta *=2
        else:
            beta /=2

        self.optimizer.apply_gradients(zip(c_grads, self.model.trainable_weights))
        self.optimizer.apply_gradients(zip(a_grads, self.model.trainable_weights))

        self.ob = []
        self.a = []
        self.ap = []
        self.r = []
        self.v = []

    def observe(self, state, action, prob_weights, reward):
        self.ob.append(state)
        self.a.append(action)
        self.ap.append(prob_weights[0])
        self.r.append(reward)

    def _discount_and_norm_rewards(self, ep_rs, end_v=0):
        discounted_ep_rs = np.zeros_like(ep_rs)
        running_add = end_v

        for t in reversed(range(0, len(ep_rs))):
            running_add = running_add * self.gamma + ep_rs[t]
            discounted_ep_rs[t] = running_add

        return discounted_ep_rs


def main():
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    agent = ProximalPolicyOptimization()
    render_flag = False
    episode = 0
    t = 0
    high = 0
    while 1:

        state = env.reset()

        sum_r = 0

        while 1:
            if render_flag:
                env.render()
            action, prob_weights = agent.choose_action(state)

            state_, reward, done, info = env.step(action)

            agent.observe(state, action, prob_weights, reward)

            sum_r += reward

            t += 1

            if done:
                if sum_r > high:
                    high = sum_r
                if high > 1000:
                    render_flag = True
                print(high)
                print(episode, sum_r)
                break

            state = state_

        agent.learn()
        episode += 1


if __name__ == '__main__':
    main()
