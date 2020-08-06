# Leetcode 743
#
# 有 N 个网络节点，标记为 1 到 N。
# 给定一个列表 times，表示信号经过有向边的传递时间
# times[i] = (u, v, w)，其中 u 是源节点，v 是目标节点， w 是一个信号从源节点传递到目标节点的时间
#
# 现在，我们从某个节点 K 发出一个信号。需要多久才能使所有节点都收到信号？
# 如果不能使所有节点收到信号，返回 -1
#
# N = 4,  K = 2
#
#      1
#   2  → 3
# 1 ↓    ↓  1       ans = 2
#   1    4

class Solution():
    def networkDelayTime(self, times, N, K):
        import collections
        import heapq
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        pq = [(0, K)]
        dist = {}
        while pq:
            d, node = heapq.heappop(pq)
            if node in dist: continue
            dist[node] = d
            for nei, d2 in graph[node]:
                if nei not in dist:
                    heapq.heappush(pq, (d + d2, nei))

        return max(dist.values()) if len(dist) == N else -1
