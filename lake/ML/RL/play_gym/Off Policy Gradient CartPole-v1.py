import gym
import numpy as np
import tensorflow as tf
import random


# modify from on-policy gradient
# According to the following formula
# J(\theta')=\sum_{t=1}^T\mathbf{E}_{\mathbf{s}_t\sim p_\theta(\mathbf{s}_t)}\left[\frac{p_{\theta'}(\mathbf{s}_t)}{p_{\theta}(\mathbf{s}_t)}\mathbf{E}_{\mathbf{a}_t\sim\pi_\theta(\mathbf{a}_t|\mathbf{s}_t)}\left[\frac{\pi_{\theta'}(\mathbf{a}_t|\mathbf{s}_t)}{\pi_{\theta}(\mathbf{a}_t|\mathbf{s}_t)}r(\mathbf{s}_t,\mathbf{a}_t)\right]\right]
# this achieve is work , but not good , because of the high variance

class OffPolicyGradient():
    def __init__(
            self,
            n_actions,
            n_features,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = 0.01
        self.gamma = 0.95
        self.memory_size = 512
        self.memory_index = 0
        # self.memory's structure
        #       1    1    1    1
        #       ob   a    r    ap
        self.memory = np.zeros((self.memory_size, 4), dtype=object)
        self.sm = []
        self.am = []
        self.apm = []
        self.rm = []
        self.batch_size = 32
        self._build_net()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.InteractiveSession(config=config)

        self.sess.run(tf.global_variables_initializer())

    def _build_net(self):
        with tf.name_scope('inputs'):
            self.ob = tf.placeholder(tf.float32, [None, self.n_features], name="observations")
            self.a = tf.placeholder(tf.int32, [None, 1], name="action")
            self.ap = tf.placeholder(tf.float32, [None, 1], name="action_probability")
            self.r = tf.placeholder(tf.float32, [None, 1], name="reward")
        # fc1
        with tf.variable_scope("parameter"):
            layer = tf.layers.dense(
                inputs=self.ob,
                units=10,
                activation=tf.nn.relu,  # tanh activation
                kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
                bias_initializer=tf.constant_initializer(0.1),
                name='fc1'
            )
            # fc2
            all_act = tf.layers.dense(
                inputs=layer,
                units=self.n_actions,
                activation=None,
                kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
                bias_initializer=tf.constant_initializer(0.1),
                name='fc3'
            )

        self.all_act_prob = tf.nn.softmax(all_act, name='act_prob')  # use softmax to convert to probability
        self.parameter = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="parameter")

        l = tf.shape(self.a)[0]

        self.batch_index = tf.expand_dims(tf.range(0, l, dtype=tf.int32), 1)
        self.action_index = tf.concat([self.batch_index, self.a], 1)

        self.J = tf.reduce_sum(
            tf.expand_dims(tf.manip.gather_nd(self.all_act_prob, self.action_index),
                           1) / self.ap * self.r) / tf.cast(l,tf.float32)

        self.grads = tf.gradients(self.J, self.parameter)

        # Because we are looking for the maximum value of J , so the learning rate is negative
        # tf.train.AdamOptimizer
        # https://www.tensorflow.org/api_docs/python/tf/train/AdamOptimizer
        self.opt = tf.train.AdamOptimizer(-self.lr)

        self.train_op = self.opt.apply_gradients(zip(self.grads, self.parameter))

    def choose_action(self, observation):
        """
        :param observation: observation
        :return: action mean what action is chosen , and
                 prob_weights[0][action] mean the probability about action which is chosen
        """
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.ob: observation[np.newaxis, :]})
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights.ravel())  # select action w.r.t the actions prob
        return action, prob_weights[0][action]

    # Store first
    def store_transition(self, s, a, ap, r):
        self.sm.append(s)
        self.am.append([a])
        self.apm.append([ap])
        self.rm.append([r])

    # after handle reward then transfer to memory
    def transfer(self):
        discounted_ep_rs_norm = self._discount_and_norm_rewards()
        index = self.memory_index % self.memory_size
        self.memory[index][0] = self.sm
        self.memory[index][1] = self.am
        self.memory[index][2] = self.apm
        self.memory[index][3] = discounted_ep_rs_norm

        self.memory_index += 1

        self.sm = []
        self.am = []
        self.apm = []
        self.rm = []

    # A little different from  on-policy gradient
    # discounted_ep_rs from np.array to list
    def _discount_and_norm_rewards(self):
        discounted_ep_rs = [[0] for _ in range(len(self.rm))]
        running_add = 0
        for t in reversed(range(0, len(self.rm))):
            running_add = running_add * self.gamma + self.rm[t][0]
            discounted_ep_rs[t][0] = running_add
        discounted_ep_rs -= np.mean(discounted_ep_rs)
        discounted_ep_rs /= np.std(discounted_ep_rs)
        return discounted_ep_rs

    def learn(self):
        if self.memory_index > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_index, size=self.batch_size)

        batch_memory = self.memory[sample_index, :]

        for i in batch_memory:
            self.sess.run(self.train_op, feed_dict={
                self.ob: i[0],
                self.a: i[1],
                self.ap: i[2],
                self.r: i[3],
            })


def main():
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    agent = OffPolicyGradient(env.action_space.n, env.observation_space.shape[0])
    max_reward = 0
    episode = 0

    # random fill. At least agent.batch_size
    i = 0
    while 1:
        observation = env.reset()
        while True:
            action, action_pro = agent.choose_action(observation)

            observation_, reward, done, info = env.step(action)
            agent.store_transition(observation, action, action_pro, reward)

            if done:
                i += 1
                agent.transfer()
                break

            observation = observation_
        if i > agent.batch_size:
            break

    while 1:
        observation = env.reset()
        one_episode_reward = 0
        while True:
            # env.render()

            action, action_pro = agent.choose_action(observation)

            observation_, reward, done, info = env.step(action)
            one_episode_reward += reward
            agent.store_transition(observation, action, action_pro, reward)

            if done:
                agent.store_transition(observation, action, action_pro, -5)
                if one_episode_reward > max_reward:
                    max_reward = one_episode_reward
                print("this episode reward is", one_episode_reward)
                print(episode)
                print(max_reward)
                agent.transfer()
                agent.learn()
                episode += 1
                break
            agent.learn()
            observation = observation_


if __name__ == '__main__':
    main()
