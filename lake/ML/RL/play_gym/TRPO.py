import gym
import numpy as np
import tensorflow as tf
from tensorflow.python.ops.parallel_for import jacobian


#
# refer : https://github.com/studywolf/blog/blob/master/tensorflow_models/npg_cartpole/natural_policy_gradient.py
#

class TrustRegionPolicyGradient:
    def __init__(
            self,
            n_actions,
            n_features,
    ):

        self.n_actions = n_actions
        self.n_features = n_features
        self.vlr = 0.1
        self.gamma = 0.97
        self.delta = 0.001
        self.alpha = 0.9
        self.transitions = []

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.InteractiveSession(config=config)
        self._build_net()
        self.sess.run(tf.global_variables_initializer())

    def _build_net(self):
        self.tf_s = tf.placeholder(tf.float32, [None, self.n_features], name="observations")
        self.tf_a = tf.placeholder(tf.float32, [None, 2], name="actions_num")
        self.tf_r = tf.placeholder(tf.float32, [None, ], name="actions_value")
        self.tf_realv = tf.placeholder(tf.float32, [None, 1], name="real_value")  # According to the sample
        self.tf_adv = tf.placeholder(tf.float32, [None, 1], name="advantages")
        self.tf_discount_update = tf.placeholder(tf.float32, [4, 2], name="discount_update")

        w_init = tf.random_normal_initializer(mean=0, stddev=0.3)
        b_init = tf.constant_initializer(0.1)

        with tf.variable_scope("value"):
            w1 = tf.get_variable("w1", [self.n_features, 10], initializer=w_init)
            b1 = tf.get_variable("b1", [10], initializer=b_init)
            l1 = tf.nn.relu(tf.matmul(self.tf_s, w1) + b1)
            w2 = tf.get_variable("w2", [10, 1], initializer=w_init)
            b2 = tf.get_variable("b2", [1], initializer=b_init)
            self.estv = tf.matmul(l1, w2) + b2

            self.v_loss = 1.00 / tf.cast(tf.shape(self.tf_realv)[0], tf.float32) \
                          * \
                          tf.reduce_sum(tf.square(self.estv - self.tf_realv))

            self.v_opt = tf.train.AdamOptimizer(self.vlr).minimize(self.v_loss)

        with tf.variable_scope("policy"):
            self.w1 = tf.get_variable("w1", [self.n_features, 2], initializer=w_init)
            self.action_t = tf.matmul(self.tf_s, self.w1)
            self.all_act_prob = tf.nn.softmax(self.action_t)

        self.policy_parameter = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="policy")

        self.action_prob = tf.reduce_sum(
            tf.multiply(self.all_act_prob, self.tf_a), reduction_indices=[1])

        action_log_prob = tf.log(self.action_prob)

        self.action_log_prob_flat = tf.reshape(action_log_prob, (-1,))

        self.g_ = tf.gradients(self.action_log_prob_flat, self.policy_parameter, grad_ys=self.tf_adv)

        self.g_log_prob_ = jacobian(self.action_log_prob_flat, self.policy_parameter[0])
        self.g_log_prob_r_ = tf.reshape(self.g_log_prob_, (-1, 8, 1))

        # self.g_log_prob = tf.gradients(self.action_log_prob_flat, self.policy_parameter[0])
        self.g_log_prob = jacobian(self.action_log_prob_flat, self.policy_parameter[0])

        self.g_log_prob_r = tf.reshape(self.g_log_prob, (-1, 8, 1))
        self.g_ = tf.reshape(self.g_, (-1, 8, 1))

        self.g = self.g_

        self.g = 1.00 / tf.cast(tf.shape(self.tf_a)[0], tf.float32) * tf.reduce_sum(self.g, reduction_indices=[0])

        self.F2 = tf.map_fn(lambda x: tf.matmul(x, tf.transpose(x)), self.g_log_prob_r)
        self.F = 1.0 / tf.cast(tf.shape(self.tf_a)[0], tf.float32) * tf.reduce_sum(self.F2, reduction_indices=[0])

        S, U, V = tf.svd(self.F)
        atol = tf.reduce_max(S) * 1e-6
        S_inv = tf.divide(1.0, S)
        S_inv = tf.where(S < atol, tf.zeros_like(S), S_inv)
        S_inv = tf.diag(S_inv)
        F_inv = tf.matmul(S_inv, tf.transpose(U))
        self.F_inv = tf.matmul(V, F_inv)

        self.F_inv_g = tf.matmul(self.F_inv, self.g)

        self.learning_rate = tf.sqrt(
            tf.divide(2 * self.delta, tf.matmul(tf.transpose(self.g), self.F_inv_g)))

        update = tf.multiply(self.learning_rate, self.F_inv_g)
        self.update = tf.reshape(update, (4, 2))

        self.add_opt = tf.assign_add(self.policy_parameter[0], self.tf_discount_update)
        self.minus_opt = tf.assign_add(self.policy_parameter[0], -self.tf_discount_update)

    def choose_action(self, observation):
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.tf_s: observation[np.newaxis, :]})

        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights[0])

        return action

    def store_transition(self, transition):
        self.transitions.append(transition)

    def learn(self):

        s = []
        a = []
        r = []
        advantage = []
        realv = []

        for i, trans in enumerate(self.transitions):
            l = len(trans)
            s_ = [0] * l
            a_ = [0] * l
            r_ = [0] * l
            for j, t in enumerate(trans):
                s_[j] = t[0]
                a_[j] = t[1]
                r_[j] = t[2]

            advantage_, realv_ = self.calc_advantages_and_realv(s_, r_)

            s.extend(s_)
            a.extend(a_)
            r.extend(r_)
            advantage.extend(advantage_)
            realv.extend(realv_)

        self.sess.run(self.v_opt, feed_dict={
            self.tf_s: np.array(s),
            self.tf_realv: np.array(realv)[:, np.newaxis]
        })

        all_act_prob,action_prob, update = self.sess.run([self.all_act_prob,self.action_prob, self.update],
                                            feed_dict={
                                                self.tf_s: np.array(s),
                                                self.tf_a: np.array(a),
                                                self.tf_adv: np.array(advantage),
                                            })

        # self.sess.run(self.add_opt, feed_dict={self.tf_discount_update: update})

        for j in range(50):
            discount_update = self.alpha ** j * update
            self.sess.run(self.add_opt, feed_dict={self.tf_discount_update: discount_update})
            new_all_act_prob, new_action_prob = self.sess.run([self.all_act_prob,self.action_prob],
                                            feed_dict={
                                                self.tf_s: np.array(s),
                                                self.tf_a: np.array(a),
                                            })

            # if j > 30:
                # print('dbg')

            DKL = np.sum(np.multiply(
                new_all_act_prob,
                np.log(
                    new_all_act_prob / (all_act_prob+1e-6)
                )
            ))

            if DKL > self.delta:
                self.sess.run(self.minus_opt, feed_dict={self.tf_discount_update: discount_update})
                continue
            else:
                L = np.sum(np.multiply(new_action_prob / action_prob, advantage)) / 500
                if L < 0:
                    self.sess.run(self.minus_opt, feed_dict={self.tf_discount_update: discount_update})
                else:
                    break

        self.transitions = []

    # def calc_advantages_and_realv(self, s, r):
    #
    #     estv = self.sess.run(self.estv, feed_dict={
    #         self.tf_s: np.array(s)
    #     })
    #
    #     realv = np.zeros_like(r)
    #     running_add = 0
    #
    #     for t in range(len(r) - 1, -1, -1):
    #         running_add = running_add * self.gamma + r[t]
    #         realv[t] = running_add
    #
    #     advantages = [0] * len(r)
    #
    #     for i in range(len(r)):
    #         advantages[i] = (realv[i] - estv[i])
    #
    #     return advantages, realv
    def calc_advantages_and_realv(self,s,r):

        estv = self.sess.run(self.estv, feed_dict={
            self.tf_s: np.array(s)
        })

        realv = np.zeros_like(r)
        running_add = 0

        for t in range(0,len(r)-1):
            realv[t] = self.gamma * estv[t+1] + r[t]

        realv[-1] = r[-1]


        advantages = [0] * len(r)

        for i in range(len(r)):
            advantages[i] = (realv[i] - estv[i])

        return advantages,realv


def main():
    env = gym.make('CartPole-v0')
    env = env.unwrapped
    agent = TrustRegionPolicyGradient(env.action_space.n, env.observation_space.shape[0])

    episode = 0
    t = 0
    max_steps = 500
    while 1:
        transition = []

        observation = env.reset()

        sum_r = 0
        reward_list = []

        while 1:

            action = agent.choose_action(observation)

            observation_, reward, done, info = env.step(action)

            sum_r += reward

            if action == 0:
                transition.append((observation, [1, 0], reward))
            else:
                transition.append((observation, [0, 1], reward))

            t += 1

            if done or t == max_steps:
                reward_list.append(sum_r)
                sum_r = 0
                agent.store_transition(transition)
                transition = []
                if done:
                    observation = env.reset()
                if t == max_steps:
                    t = 0
                    env.close()
                    episode += 1
                    print(episode)
                    print(reward_list)
                    break

            observation = observation_

        agent.learn()


if __name__ == '__main__':
    main()
