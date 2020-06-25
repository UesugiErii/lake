import gym
import numpy as np
import tensorflow as tf


def main():


    class DQN():
        def __init__(self):
            self.n_actions = 2
            self.n_features = 4
            self.learning_rate = 0.001
            self.gamma = 0.98
            self.replace_target_iter = 100
            self.memory_index = 0
            self.memory_size = 20000
            self.memory = np.zeros((self.memory_size, self.n_features + 1 + 1 )).astype('float32')
            self.batch_size = 512
            self.learn_step_counter = 0
            self.sess = tf.Session()
            self._create_model()
            self.sess.run(tf.global_variables_initializer())
            self.ep_obs, self.ep_as, self.ep_rs = [], [], []

        def _create_model(self):
            with tf.name_scope('inputs'):
                self.tf_obs = tf.placeholder(tf.float32, [None, self.n_features], name="observations")
                self.tf_acts = tf.placeholder(tf.int32, [None, ], name="actions_num")
                self.tf_vt = tf.placeholder(tf.float32, [None, ], name="actions_value")
            # fc1
            layer = tf.layers.dense(
                inputs=self.tf_obs,
                units=10,
                activation=tf.nn.tanh,  # tanh activation
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

            with tf.name_scope('loss'):
                # to maximize total reward (log_p * R) is to minimize -(log_p * R), and the tf only have minimize(loss)
                neg_log_prob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=all_act,
                                                                              labels=self.tf_acts)  # this is negative log of chosen action
                # or in this way:
                # neg_log_prob = tf.reduce_sum(-tf.log(self.all_act_prob)*tf.one_hot(self.tf_acts, self.n_actions), axis=1)
                loss = tf.reduce_mean(neg_log_prob * self.tf_vt)  # reward guided loss

            with tf.name_scope('train'):
                self.train_op = tf.train.AdamOptimizer(self.learning_rate).minimize(loss)



        def choose_action(self, obs):
            prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.tf_obs: obs[np.newaxis, :]})
            action = np.random.choice(range(prob_weights.shape[1]),
                                      p=prob_weights.ravel())  # select action w.r.t the actions prob
            return action

        def store_transition(self, s0, action, reward):
            self.ep_obs.append(s0)
            self.ep_as.append(action)
            self.ep_rs.append(reward)

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
            # discount episode rewards
            discounted_ep_rs = np.zeros_like(self.ep_rs)
            running_add = 0
            for t in reversed(range(0, len(self.ep_rs))):
                running_add = running_add * self.gamma + self.ep_rs[t]
                discounted_ep_rs[t] = running_add

            # normalize episode rewards
            discounted_ep_rs -= np.mean(discounted_ep_rs)
            discounted_ep_rs /= np.std(discounted_ep_rs)
            return discounted_ep_rs



    agent = DQN()
    episode = 0
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    max_reward = 0
    RENDER= False
    while 1:

        obs = env.reset()
        one_episode_reward = 0

        while 1:
            # if episode > 150:
            #     RENDER = True
            # if RENDER:
            #     env.render()
            action = agent.choose_action(obs)


            obs_, reward, is_finished, info = env.step(action)
            one_episode_reward += reward
            x, x_dot, theta, theta_dot = obs_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            reward = r1 + r2
            agent.store_transition(obs, action, reward)
            if is_finished:
                # agent.store_transition(obs, action, -100, obs_)
                if one_episode_reward > max_reward:
                    max_reward = one_episode_reward
                print('this episode reward is',one_episode_reward)
                agent.learn()
                break


            obs = obs_
        episode += 1
        print(episode)
        print(max_reward)

if __name__ == '__main__':
    main()
