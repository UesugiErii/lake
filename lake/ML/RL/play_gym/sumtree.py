import numpy

# origin : https://github.com/jaara/AI-blog/blob/master/SumTree.py

class SumTree:
    write = 0

    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = numpy.zeros( 2*capacity - 1 )
        self.data = numpy.zeros( capacity, dtype=object )

    def _propagate(self, idx, change):
        parent = (idx - 1) // 2

        self.tree[parent] += change

        if parent != 0:
            self._propagate(parent, change)

    # def _retrieve(self, idx, s):
    #     left = 2 * idx + 1
    #     right = left + 1
    #
    #     if left >= len(self.tree):
    #         return idx
    #
    #     if s <= self.tree[left]:
    #         return self._retrieve(left, s)
    #     else:
    #         return self._retrieve(right, s-self.tree[left])

    def total(self):
        return self.tree[0]

    def add(self, p, data):
        idx = self.write + self.capacity - 1

        self.data[self.write] = data
        self.update(idx, p)

        self.write += 1
        if self.write >= self.capacity:
            self.write = 0

    def update(self, idx, p):
        change = p - self.tree[idx]

        self.tree[idx] = p
        self._propagate(idx, change)

    def get(self, s):
        # idx = self._retrieve(0, s)
        # dataIdx = idx - self.capacity + 1
        #
        # return (idx, self.tree[idx], self.data[dataIdx])

        # origin : https://morvanzhou.github.io/tutorials/machine-learning/reinforcement-learning/4-6-prioritized-replay/
        parent_idx = 0
        while True:     # the while loop is faster than the method in the reference code
            cl_idx = 2 * parent_idx + 1         # this leaf's left and right kids
            cr_idx = cl_idx + 1
            if cl_idx >= len(self.tree):        # reach bottom, end search
                leaf_idx = parent_idx
                break
            else:       # downward search, always search for a higher priority node
                if s <= self.tree[cl_idx]:
                    parent_idx = cl_idx
                else:
                    s -= self.tree[cl_idx]
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return (leaf_idx, self.tree[leaf_idx], self.data[data_idx])
