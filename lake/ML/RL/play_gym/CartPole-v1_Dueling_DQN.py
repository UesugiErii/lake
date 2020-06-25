import gym
import numpy as np
import tensorflow as tf


def main():


    class DQN():
        def __init__(self):
            self.n_actions = 2
            self.n_features = 4
            self.learning_rate = 0.01
            self.gamma = 0.9
            self.replace_target_iter = 100
            self.memory_index = 0
            self.memory_size = 20000
            self.memory = np.zeros((self.memory_size, self.n_features * 2 + 1 + 1 )).astype('float32')
            self.batch_size = 1024
            self.learn_step_counter = 0
            self.sess = tf.Session()
            self._create_model()
            self.t_params = tf.get_collection('target_net_params')
            self.e_params = tf.get_collection('eval_net_params')
            self.replace_target_op = [tf.assign(t, e) for t, e in zip(self.t_params, self.e_params)]

            # self.summary_writer = tf.summary.FileWriter(logdir='/media/zx/8ACAF3CECAF3B493/tfb', graph=self.sess.graph)
            self.merged = tf.summary.merge_all()
            self.sess.run(tf.global_variables_initializer())

        def _create_model(self):
            self.s0 = tf.placeholder(tf.float32, [None, self.n_features], name='s0')  # input
            self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='Q_target')  # for calculating loss
            with tf.variable_scope('eval_net'):
                c_names, n_l1, w_initializer, b_initializer = \
                    ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 10, \
                    tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers

                with tf.variable_scope('l1'):
                    w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                    b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                    l1 = tf.nn.relu(tf.matmul(self.s0, w1) + b1)
                    tf.summary.histogram('w1', w1)
                    tf.summary.histogram('b1', b1)
                with tf.variable_scope('l2'):
                    with tf.variable_scope('Value'):
                        w2 = tf.get_variable('w2', [n_l1, 1], initializer=w_initializer, collections=c_names)
                        b2 = tf.get_variable('b2', [1, 1], initializer=b_initializer, collections=c_names)
                        self.V = tf.matmul(l1, w2) + b2

                    with tf.variable_scope('Advantage'):
                        w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer,
                                             collections=c_names)
                        b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                        self.A = tf.matmul(l1, w2) + b2
                    self.q_eval = self.V + self.A - tf.reduce_mean(self.A, axis=1, keep_dims=True)


            self.s1 = tf.placeholder(tf.float32, [None, self.n_features], name='s1')  # input
            with tf.variable_scope('target_net'):
                c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]

                with tf.variable_scope('l1'):
                    w1 = tf.get_variable('w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                    b1 = tf.get_variable('b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                    l1 = tf.nn.relu(tf.matmul(self.s1, w1) + b1)
                    tf.summary.histogram('w1', w1)
                    tf.summary.histogram('b1', b1)

                with tf.variable_scope('l2'):
                    with tf.variable_scope('Value'):
                        w2 = tf.get_variable('w2', [n_l1, 1], initializer=w_initializer, collections=c_names)
                        b2 = tf.get_variable('b2', [1, 1], initializer=b_initializer, collections=c_names)
                        self.V = tf.matmul(l1, w2) + b2

                    with tf.variable_scope('Advantage'):
                        w2 = tf.get_variable('w2', [n_l1, self.n_actions], initializer=w_initializer,
                                             collections=c_names)
                        b2 = tf.get_variable('b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                        self.A = tf.matmul(l1, w2) + b2
                    self.q_next = self.V + self.A - tf.reduce_mean(self.A, axis=1, keep_dims=True)

            with tf.variable_scope('loss'):
                self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
                tf.summary.scalar('loss', self.loss)
            with tf.variable_scope('train'):
                self._train_op = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)



        def choose_action(self, obs):
            obs = obs[np.newaxis, :]
            if np.random.random() < 100/(self.learn_step_counter+1):
                return np.random.choice((0,1))
            else:
                actions_value = self.sess.run(self.q_eval, feed_dict={self.s0: obs})
                if self.learn_step_counter % 1000 == 0:
                    print(actions_value)
                x = np.argmax(actions_value)
                return x

        def store_transition(self, s0, action, reward, s1):
            """
                s0              :4
                action_num      4
                reward          5
                s1              -4:
            """
            transition = np.hstack((s0.reshape((1, self.n_features)),
                                    np.array([[action]]),
                                    np.array([[reward]]),
                                    s1.reshape((1, self.n_features))))
            self.memory[self.memory_index % self.memory_size, :] = transition
            self.memory_index += 1

        def learn(self):
            if self.learn_step_counter % self.replace_target_iter == 3:
                self.sess.run(self.replace_target_op)
            if self.memory_index > self.memory_size:
                sample_index = np.random.choice(self.memory_size, size=self.batch_size)
            else:
                sample_index = np.random.choice(self.memory_index, size=self.batch_size)
            batch_memory = self.memory[sample_index, :]
            q_next, q_eval = self.sess.run(
                [self.q_next, self.q_eval],
                feed_dict={
                    self.s1: batch_memory[:, -self.n_features:],  # fixed params
                    self.s0: batch_memory[:, :self.n_features],  # newest params
                })
            q_target = q_eval.copy()
            batch_index = np.arange(self.batch_size, dtype=np.int32)
            eval_act_index = batch_memory[:, self.n_features].astype(int)
            reward = batch_memory[:, self.n_features + 1]
            q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)
            summary, _, self.lost = self.sess.run([self.merged, self._train_op, self.loss],
                                                  feed_dict={self.s0: batch_memory[:, :self.n_features],
                                                             self.q_target: q_target})


            #
            # if self.learn_step_counter%500 ==0:
            #     self.summary_writer.add_summary(summary, self.learn_step_counter)

            self.learn_step_counter += 1



    agent = DQN()
    total_step = 0
    episode = 0
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    max_reward = 0
    while 1:


        obs = env.reset()
        one_episode_reward = 0

        while 1:
            env.render()
            action = agent.choose_action(obs)


            obs_, reward, is_finished, info = env.step(action)
            one_episode_reward += reward
            x, x_dot, theta, theta_dot = obs_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            reward = r1 + r2

            if is_finished:
                # agent.store_transition(obs, action, -100, obs_)
                if one_episode_reward > max_reward:
                    max_reward = one_episode_reward
                print('this episode reward is',one_episode_reward)
                break


            agent.store_transition(obs, action, reward, obs_)
            if total_step > 300:
                agent.learn()
            total_step += 1
            obs = obs_
        episode += 1
        print(episode)
        print(max_reward)

if __name__ == '__main__':
    main()
