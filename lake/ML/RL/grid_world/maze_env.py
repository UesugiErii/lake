import numpy as np
import time
import tkinter as tk

UNIT = 40  # The number of pixels occupied by the sides of the grid
Eage = 5  # The number of pixels occupied by the eage
half_UNIT = UNIT // 2
half_LEN = UNIT // 2 - Eage
MAZE_H = 8  # grid world height
MAZE_W = 8  # grid world width
hell_list = [[5, 6], [4, 5], [5, 4], [7, 5]]  # hell coordinate
# hell_list = []
oval_list = [[5, 5]]  # oval coordinate


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['w', 'a', 's', 'd']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self.hell_list = []
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([half_UNIT, half_UNIT])

        # hell
        for hell in hell_list:
            hell_center = origin + np.array([(hell[0] - 1) * UNIT, (hell[1] - 1) * UNIT])
            self.hell = self.canvas.create_rectangle(
                hell_center[0] - half_LEN, hell_center[1] - half_LEN,
                hell_center[0] + half_LEN, hell_center[1] + half_LEN,
                fill='black')

        # create oval
        for oval in oval_list:
            oval_center = origin + [(oval[0] - 1) * UNIT, (oval[1] - 1) * UNIT]
            self.oval = self.canvas.create_oval(
                oval_center[0] - half_LEN, oval_center[1] - half_LEN,
                oval_center[0] + half_LEN, oval_center[1] + half_LEN,
                fill='yellow')

        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - half_LEN, origin[1] - half_LEN,
            origin[0] + half_LEN, origin[1] + half_LEN,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([half_UNIT, half_UNIT])
        self.rect = self.canvas.create_rectangle(
            origin[0] - half_LEN, origin[1] - half_LEN,
            origin[0] + half_LEN, origin[1] + half_LEN,
            fill='red')
        # return observation
        return index_to_index(self.canvas.coords(self.rect))

    def step(self, action):
        s0 = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 'w':  # up
            if s0[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 's':  # down
            if s0[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 'd':  # right
            if s0[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 'a':  # left
            if s0[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s1 = self.canvas.coords(self.rect)  # next state
        s1 = index_to_index(s1)
        # reward function
        if s1 in oval_list:
            reward = 10
            done = True
            s1 = 'terminal'
        elif s1 in hell_list:
            reward = -10
            done = True
            s1 = 'terminal'
        else:
            reward = -1
            done = False

        return s1, reward, done

    def render(self):
        # time.sleep(0.04)
        self.update()


def index_to_index(index):
    return [int((index[0] - Eage) // UNIT + 1), int((index[1] - Eage) // UNIT + 1)]


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 'd'
            s, r, done = env.step(a)
            if done:
                break


if __name__ == '__main__':
    env = Maze()
    env.after(100, update)
    env.mainloop()
