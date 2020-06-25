import gym
import numpy as np
import tensorflow as tf


# modify from PG/PolicyGradient CartPole-v1.py
# the difference is that use another way to calculate gradient
# this approach is easy to understand
# According to the following formula
# \nabla_\theta J(\theta)\approx\frac{1}{N}\sum_{i=1}^N\sum_{t=1}^T\left[\nabla_\theta\log \pi_\theta(\mathbf{a}_{i,t}|\mathbf{s}_{i,t})\left(\sum_{t'=t}^Tr(\mathbf{s}_{i,t'},\mathbf{a}_{i,t'})\right)\right]
# \nabla_\theta J(\theta)=\mathbf{E}_{\tau\sim p_\theta(\tau)}[\nabla_\theta \log p_\theta(\tau)(r(\tau)-\frac{1}{N}\sum_{i=1}^Nr(\tau_i))]

class PolicyGradientV2():
    def __init__(
            self,
            n_actions,
            n_features,
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = 0.01
        self.gamma = 0.95
        self.ep_obs, self.ep_as, self.ep_rs = [], [], []
        self._build_net()
        # Limit tensorflow memory usage
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=config)
        self.sess.run(tf.global_variables_initializer())

    def _build_net(self):
        with tf.name_scope('inputs'):
            self.tf_obs = tf.placeholder(tf.float32, [None, self.n_features], name="observations")
            self.tf_acts = tf.placeholder(tf.int32, [None, ], name="actions_num")
            self.tf_vt = tf.placeholder(tf.float32, [None, ], name="actions_value")
        with tf.variable_scope("parameter"):
            # fc1
            layer = tf.layers.dense(
                inputs=self.tf_obs,
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
                name='fc2'
            )

        self.all_act_prob = tf.nn.softmax(all_act, name='act_prob')  # use softmax to convert to probability
        self.parameter = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="parameter")
        self.batch_size = tf.shape(self.tf_obs)[0]  # not fixed
        self.batch_index = tf.expand_dims(tf.range(0, self.batch_size, dtype=tf.int32), 1)
        self.action_index = tf.concat([self.batch_index, tf.expand_dims(self.tf_acts, 1)], 1)

        self.J = tf.reduce_sum(
            tf.log(tf.manip.gather_nd(self.all_act_prob, self.action_index)) * self.tf_vt) / tf.cast(self.batch_size,
                                                                                                     dtype=tf.float32)

        self.grads = tf.gradients(self.J, self.parameter)

        self.opt = tf.train.AdamOptimizer(-self.lr)

        self.train_op = self.opt.apply_gradients(zip(self.grads, self.parameter))

    def choose_action(self, observation):
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.tf_obs: observation[np.newaxis, :]})
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights.ravel())  # select action w.r.t the actions prob
        return action

    def store_transition(self, s, a, r):
        self.ep_obs.append(s)
        self.ep_as.append(a)
        self.ep_rs.append(r)

    def learn(self):
        # discount and normalize episode reward
        discounted_ep_rs_norm = self._discount_and_norm_rewards()

        # train on episode
        self.sess.run(self.train_op, feed_dict={
            self.tf_obs: np.vstack(self.ep_obs),  # shape=[None, n_obs]
            self.tf_acts: np.array(self.ep_as),  # shape=[None, ]
            self.tf_vt: discounted_ep_rs_norm,  # shape=[None, ]
        })

        self.ep_obs, self.ep_as, self.ep_rs = [], [], []  # empty episode data
        return discounted_ep_rs_norm

    def _discount_and_norm_rewards(self):
        # this function use two way to reduce variance in CS294
        # one is use casuality
        # another is baseline
        discounted_ep_rs = np.zeros_like(self.ep_rs)
        running_add = 0

        # casuality
        for t in reversed(range(0, len(self.ep_rs))):
            running_add = running_add * self.gamma + self.ep_rs[t]
            discounted_ep_rs[t] = running_add
        # presume I walked 5 steps(t=[0,5) ) , and I get a big reward in t=3
        # so when t = 0,1,2 , the action is good ,since I can get a big reward in t=3
        # and what I do in t=4 don't affect reward when t=3
        # so main idea is the future does not affect the present

        # normalize episode rewards
        discounted_ep_rs -= np.mean(discounted_ep_rs)
        discounted_ep_rs /= np.std(discounted_ep_rs)
        return discounted_ep_rs


def main():
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    agent = PolicyGradientV2(env.action_space.n, env.observation_space.shape[0])
    max_reward = 0
    episode = 0
    while 1:

        observation = env.reset()
        one_episode_reward = 0
        while True:
            # env.render()

            action = agent.choose_action(observation)

            observation_, reward, done, info = env.step(action)
            one_episode_reward += reward
            agent.store_transition(observation, action, reward)

            if done:
                if one_episode_reward > max_reward:
                    max_reward = one_episode_reward
                print("this episode reward is", one_episode_reward)
                print(episode)
                print(max_reward)
                vt = agent.learn()
                episode += 1
                break

            observation = observation_


if __name__ == '__main__':
    main()
