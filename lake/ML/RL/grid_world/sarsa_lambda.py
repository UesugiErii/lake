from sarsa import SARSA
import random


class SARSA_LAMBDA(SARSA):
    def __init__(self):
        super().__init__()
        self.E = {}
        self.lambda_ = 1

    def learning(self, s0, a0, reward, s1, a1):
        s0, s1 = str(s0), str(s1)
        delta = reward + self.gamma * self._get(self.Q, s1, a1) - self._get(self.Q, s0, a0)
        self._set(self.E, s0, a0, self._get(self.E, s0, a0) + 1)
        for s, a_map_v in self.E.items():
            for a, v in a_map_v.items():
                self._set(self.Q, s, a, self._get(self.Q, s, a) + self.alpha * delta * self._get(self.E, s, a))
                self._set(self.E, s, a, self.gamma * self.lambda_ * self._get(self.E, s, a))


if __name__ == '__main__':
    a = SARSA_LAMBDA()
