# Leetcode 1514

class P():
    def __init__(self, index, prob):
        self.index = index
        self.prob = prob

    def __lt__(self, other):
        # Because we need the greatest probability, we need to modify the comparison function
        # change default min heap to max heap
        return self.prob > other.prob


class Solution:
    def maxProbability(self, n: int, edges, succProb, start: int, end: int) -> float:
        import heapq
        # The default is min heap
        from collections import defaultdict

        g = defaultdict(dict)
        for i, edge in enumerate(edges):
            g[edge[0]][edge[1]] = succProb[i]
            g[edge[1]][edge[0]] = succProb[i]

        prob = [0] * n
        prob[start] = 1
        h = []
        heapq.heappush(h, P(start, 1))
        min_ = set()  # Already the biggest
        while h:
            temp = heapq.heappop(h)
            i = temp.index
            min_.add(i)
            p = temp.prob
            for j in g[i].keys():
                if j in min_:
                    continue
                pij = g[i][j]
                if pij * p > prob[j]:
                    prob[j] = p * pij
                    heapq.heappush(h, P(j, prob[j]))
        return prob[end]


print(Solution().maxProbability(n=3, edges=[[0, 1], [1, 2], [0, 2]], succProb=[0.5, 0.5, 0.2], start=0, end=2))
