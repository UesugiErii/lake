from maze_env import Maze
from sarsa import SARSA
from sarsa_lambda import SARSA_LAMBDA
from q_learning import Q_learning

def on_policy():
    success = 0
    fail = 0
    for episode in range(200):
        # 初始化环境
        s0 = env.reset()
        # Sarsa 根据 state 观测选择行为
        a0 = agent.get_action(s0, episode)
        path = a0
        while True:

            # 刷新环境
            env.render()

            # 在环境中采取行为, 获得下一个 state_ (obervation_), reward, 和是否终止
            s1, reward, done = env.step(a0)

            # 根据下一个 state (obervation_) 选取下一个 action_
            a1 = agent.get_action(s1, episode)

            # 从 (s, a, r, s', a') 中学习, 更新 Q_tabel 的参数 ==> Sarsa
            # RL.learn(str(observation), action, reward, str(observation_), action_)
            agent.learning(s0, a0, reward, s1, a1)

            # 将下一个当成下一步的 state (observation) and action
            s0, a0 = s1, a1

            # 终止时跳出循环
            if done:
                if reward < 0:
                    print("\033[0;31;40m\t{}\033[0m".format(path))
                    fail += 1
                else:
                    print("\033[0;32;40m\t{}\033[0m".format(path))
                    success += 1
                break
            path += a1

    # 大循环完毕
    print('game over')
    print('success:', success)
    print('fail:', fail)
    env.destroy()

def q_learning():
    success = 0
    fail = 0
    for episode in range(200):

        s0 = env.reset()
        path = ''

        while True:
            env.render()

            a0 = agent.get_action(s0, episode)
            path += a0

            s1, reward, done = env.step(a0)
            a1 = agent.get_action(s1, episode)


            agent.learning(s0, a0, reward, s1, a1)

            s0= s1

            if done:
                if reward < 0:
                    print("\033[0;31;40m\t{}\033[0m".format(path))
                    fail += 1
                else:
                    print("\033[0;32;40m\t{}\033[0m".format(path))
                    success += 1
                break


    print('game over')
    print('success:', success)
    print('fail:', fail)
    env.destroy()



if __name__ == "__main__":
    env = Maze()
    # agent = SARSA()
    # agent = SARSA_LAMBDA()
    # env.after(100, on_policy)
    agent = Q_learning()
    env.after(100,q_learning)
    env.mainloop()
