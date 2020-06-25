import tensorflow as tf
import numpy as np
import gym


def main():
    class DDPG():
        def __init__(self):
            self.learning_rate = 0.001
            self.gamma = 0.9
            self.decay = 0.99
            self.memory_size = 20000
            self.memory_index = 0
            self.memory = np.zeros((self.memory_size, 8), dtype=np.float32)
            self.batch_size = 128
            self.learn_step = 0

            self.sess = tf.Session()
            self.s0 = tf.placeholder(tf.float32, [None, 3], 's0')
            self.s1 = tf.placeholder(tf.float32, [None, 3], 's1')
            self.r = tf.placeholder(tf.float32, [None, 1], 'r')
            self.ai = tf.placeholder(tf.float32, [None, 1], 'a')

            self.w_initializer = tf.random_normal_initializer(0., 0.3)
            self.b_initializer = tf.constant_initializer(0.1)


            self.a = self._create_actor(self.s0, trainable=True)
            self.q = self._create_critic(self.s0, self.a,trainable=True)
            self.qi = self._create_critic(self.s0, self.ai,reuse=True,trainable=True)

            self.actor_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='actor')
            self.critic_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='critic')

            ema = tf.train.ExponentialMovingAverage(decay=0.99)

            def ema_getter(getter, name, *args, **kwargs):
                return ema.average(getter(name, *args, **kwargs))

            self.soft_update_op = [ema.apply(self.critic_params), ema.apply(self.actor_params)]


            self.a_ = self._create_actor(self.s1, reuse=True, custom_getter=ema_getter, trainable=False)
            self.q_ = self._create_critic(self.s1, self.a_, reuse=True, custom_getter=ema_getter,
                                                  trainable=False)


            self.target_q = self.r + self.gamma * self.q_
            self.critic_error = tf.losses.mean_squared_error(labels=self.target_q, predictions=self.qi)
            self.train_critic = tf.train.AdamOptimizer(self.learning_rate).minimize(self.critic_error, var_list=self.critic_params)

            self.actor_loss = -tf.reduce_mean(self.q)
            tf.summary.scalar('actor_loss',self.actor_loss)
            self.train_actor = tf.train.AdamOptimizer(self.learning_rate).minimize(self.actor_loss, var_list=self.actor_params)

            # with tf.control_dependencies([train_critic,train_actor]):
            #     self.tr_op = ema.apply([critic_params, actor_params])
            self.summary_writer = tf.summary.FileWriter(logdir='/home/zx/.cache/tfb', graph=self.sess.graph)
            self.merged = tf.summary.merge_all()
            self.sess.run(tf.global_variables_initializer())
            print('use to dbg')

        def _create_actor(self, s, reuse=None, custom_getter=None, trainable=False):
            with tf.variable_scope('actor', reuse=reuse, custom_getter=custom_getter):
                with tf.variable_scope('l1'):
                    w1 = tf.get_variable('w1', [3, 20], trainable=trainable, initializer=self.w_initializer)
                    b1 = tf.get_variable('b1', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l1 = tf.nn.relu(tf.matmul(s, w1) + b1)
                    tf.summary.histogram('w1', w1)
                    tf.summary.histogram('b1', b1)
                with tf.variable_scope('l2'):
                    w2 = tf.get_variable('w2', [20, 20], trainable=trainable, initializer=self.w_initializer)
                    b2 = tf.get_variable('b2', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l2 = tf.nn.relu(tf.matmul(l1, w2) + b2)
                    tf.summary.histogram('w2', w2)
                    tf.summary.histogram('b2', b2)
                with tf.variable_scope('l3'):
                    w3 = tf.get_variable('w3', [20, 20], trainable=trainable, initializer=self.w_initializer)
                    b3 = tf.get_variable('b3', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l3 = tf.nn.relu(tf.matmul(l2, w3) + b3)
                    tf.summary.histogram('w3', w3)
                    tf.summary.histogram('b3', b3)
                with tf.variable_scope('l4'):
                    w4 = tf.get_variable('w4', [20, 1], trainable=trainable, initializer=self.w_initializer)
                    b4 = tf.get_variable('b4', [1, 1], trainable=trainable, initializer=self.b_initializer)
                    l4 = tf.nn.tanh(tf.matmul(l3, w4) + b4)
                    tf.summary.histogram('w4', w4)
                    tf.summary.histogram('b4', b4)
                return l4 * 2

        def _create_critic(self, s, a, reuse=None, custom_getter=None, trainable=False):
            input = tf.concat([s, a], 1)

            with tf.variable_scope('critic', reuse=reuse, custom_getter=custom_getter):
                with tf.variable_scope('l1'):
                    w1 = tf.get_variable('w1', [4, 20], trainable=trainable, initializer=self.w_initializer)
                    b1 = tf.get_variable('b1', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l1 = tf.nn.relu(tf.matmul(input, w1) + b1)
                    tf.summary.histogram('w1', w1)
                    tf.summary.histogram('b1', b1)
                with tf.variable_scope('l2'):
                    w2 = tf.get_variable('w2', [20, 20], trainable=trainable, initializer=self.w_initializer)
                    b2 = tf.get_variable('b2', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l2 = tf.nn.relu(tf.matmul(l1, w2) + b2)
                    tf.summary.histogram('w2', w2)
                    tf.summary.histogram('b2', b2)
                with tf.variable_scope('l3'):
                    w3 = tf.get_variable('w3', [20, 20], trainable=trainable, initializer=self.w_initializer)
                    b3 = tf.get_variable('b3', [1, 20], trainable=trainable, initializer=self.b_initializer)
                    l3 = tf.nn.relu(tf.matmul(l2, w3) + b3)
                    tf.summary.histogram('w3', w3)
                    tf.summary.histogram('b3', b3)
                with tf.variable_scope('l4'):
                    w4 = tf.get_variable('w4', [20, 1], trainable=trainable, initializer=self.w_initializer)
                    b4 = tf.get_variable('b4', [1, 1], trainable=trainable, initializer=self.b_initializer)
                    q = tf.matmul(l3, w4) + b4
                    tf.summary.histogram('w4', w4)
                    tf.summary.histogram('b4', b4)
                return q



        def choose_action(self, s):
            return self.sess.run(self.a, {self.s0: s[np.newaxis, :]})[0]

        def store_transition(self, s0, a, r, s1):
            transition = np.hstack((s0, a, r, s1))
            self.memory[self.memory_index % self.memory_size, :] = transition
            self.memory_index += 1

        def learn(self):
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
            batch_memory = self.memory[sample_index, :]
            s0 = batch_memory[:, :3]
            a = batch_memory[:,3][:,np.newaxis]
            r = batch_memory[:,4][:,np.newaxis]
            s1 = batch_memory[:, -3:]
            self.sess.run(self.train_critic, {self.s0: s0, self.ai: a, self.r: r, self.s1: s1})
            summary,_ = self.sess.run([self.merged,self.train_actor], {self.s0: s0})
            if self.learn_step%50 ==0:
                self.summary_writer.add_summary(summary, self.learn_step)
            self.learn_step += 1
            self.sess.run(self.soft_update_op)


    env = gym.make('Pendulum-v0')  # https://github.com/openai/gym/wiki/Pendulum-v0
    env = env.unwrapped

    agent = DDPG()

    episode = 0
    max_reward = -1000

    # random sample
    s0 = env.reset()
    for i in range(agent.memory_size):
        a = np.random.uniform(-2, 2, (1,))
        s1, r, done, info = env.step(a)
        agent.store_transition(s0, a, r, s1)
        s0 = s1

    while 1:
        total_reward = 0


        s0 = env.reset()
        for i in range(300):
            # env.render()
            a = agent.choose_action(s0)
            # print(a)
            s1, r, done, info = env.step(a)
            total_reward += r
            agent.store_transition(s0, a, r, s1)
            agent.learn()
            s0 = s1
        else:
            if total_reward > max_reward:
                max_reward = total_reward
            print(episode)
            episode += 1
            print(total_reward)
            print(max_reward)
            print('-------------------------')


if __name__ == '__main__':
    main()
