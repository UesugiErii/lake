# Leetcode 323
# 给定编号从 0 到 n-1 的 n 个节点和一个无向边列表（每条边都是一对节点），
# 请编写一个函数来计算无向图中连通分量的数目
#
# n = 5 和 edges = [[0, 1], [1, 2], [3, 4]]
#
# 0      3
# |      |       ans = 2
# 1---2  4
#
# n = 5 和 edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
#
# 0       4
# |       |      ans = 1
# 1---2---3
#
#
# 你可以假设在 edges 中不会出现重复的边。而且由于所以的边都是无向边，
# [0, 1] 与 [1, 0]  相同，所以它们不会同时在 edges 中出现

from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        parent = {}
        rank = {}
        count = n

        def find(x):
            parent.setdefault(x, x)
            # Path compression
            if x != parent[x]:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            nonlocal count
            x_root, y_root = find(x), find(y)
            if x_root == y_root: return
            # Union by rank
            if rank.setdefault(x_root, 1) < rank.setdefault(y_root, 1):
                parent[x_root] = y_root
                del rank[x_root]
            elif rank.setdefault(x_root, 1) > rank.setdefault(y_root, 1):
                parent[y_root] = x_root
                del rank[y_root]
            else:
                parent[y_root] = x_root
                rank[x_root] += 1
                del rank[y_root]
            count -= 1

        for edge in edges:
            union(edge[0], edge[1])

        return count
