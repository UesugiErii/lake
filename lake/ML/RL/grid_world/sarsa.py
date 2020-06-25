import random
from maze_env import MAZE_H, MAZE_W


class SARSA():
    def __init__(self):
        self.Q = {}
        self.action_space = ['w', 'a', 's', 'd']
        self.alpha = 0.1
        self.gamma = 0.9

    def _get(self, table, s, a):
        if not table.get(s):
            table[s] = {'w': 0, 'a': 0, 's': 0, 'd': 0}
        return table[s][a]

    def _set(self, table, s, a, value):
        if not table.get(s):
            table[s] = {'w': 0, 'a': 0, 's': 0, 'd': 0}
        table[s][a] = value

    def get_action(self, s, episode_num):
        # print(s)
        s = str(s)
        epsilon = 1 / (episode_num + 1)
        random_value = random.random()
        if random_value < epsilon:
            action = random.choice(self.action_space)
        else:
            if self.Q.get(s):
                action = max(self.Q.get(s).items(), key=lambda x: x[1])[0]
            else:
                self.Q[s] = {'w': 0, 'a': 0, 's': 0, 'd': 0}
                action = random.choice(self.action_space)
        return action

    def learning(self, s0, a0, reward, s1, a1):
        s0, s1 = str(s0), str(s1)
        old_q = self._get(self.Q, s0, a0)
        new_q = old_q + self.alpha * (reward + self.gamma * self._get(self.Q, s1, a1) - old_q)
        self._set(self.Q, s0, a0, new_q)

    # def __action_space(self, s,action_flag):
    #     str_s =str(s)
    #     if s == 'terminal':
    #         return ''
    #     temp = {'w': 0, 'a': 0, 's': 0, 'd': 0}
    #     if 2 <= s[0] <= MAZE_W - 1 and s[1] == 1:  # 上边界
    #         temp = {'a': 0, 's': 0, 'd': 0}
    #     if 2 <= s[1] <= MAZE_H - 1 and s[0] == 1:  # 左边界
    #         temp = {'w': 0, 's': 0, 'd': 0}
    #     if 2 <= s[0] <= MAZE_W - 1 and s[1] == MAZE_H:  # 下边界
    #         temp = {'a': 0, 'd': 0, 'w': 0}
    #     if 2 <= s[1] <= MAZE_W - 1 and s[0] == MAZE_W:  # 右边界
    #         temp = {'a': 0, 's': 0, 'w': 0}
    #     if s[0] == 1 and s[1] == 1:
    #         temp = {'s': 0, 'd': 0}
    #     if s[0] == 1 and s[1] == MAZE_H:
    #         temp = {'w': 0, 'd': 0}
    #     if s[0] == MAZE_W and s[1] == 1:
    #         temp = {'s': 0, 'a': 0}
    #     if s[0] == MAZE_W and s[1] == MAZE_H:
    #         temp = {'a': 0, 'w': 0}
    #     if action_flag:
    #         return random.choice(list(temp.keys()))
    #     else:
    #         self.Q[str_s] = temp
    #
    #
    # def get_action(self, s, episode_num):
    #     # print(s)
    #     str_s = str(s)
    #     epsilon = 1 / (episode_num + 1)
    #     random_value = random.random()
    #     if random_value < epsilon:
    #         action = self.__action_space(s,True)
    #     else:
    #         if self.Q.get(str_s):
    #             action = max(self.Q.get(str_s).items(), key=lambda x: x[1])[0]
    #         else:
    #             self.__action_space(s,False)
    #
    #             action = self.__action_space(s,True)
    #     return action
    #
    # def learning(self, s0, a0, reward, s1, a1):
    #     if s1 == 'terminal':
    #         return None
    #     str_s0, str_s1 = str(s0), str(s1)
    #     if not self.Q.get(str_s1):
    #         self.__action_space(s1,False)
    #     if not self.Q.get(str_s0):
    #         self.__action_space(s0,False)
    #     self.Q[str_s0][a0] = self.Q[str_s0][a0] + self.alpha * (
    #                 reward + self.gamma * self.Q[str_s1][a1] - self.Q[str_s0][a0])
