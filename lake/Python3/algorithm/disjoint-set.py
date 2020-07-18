# Leetcode 547

class Solution:
    def findCircleNum(self, M: List[List[int]]) -> int:
        parent = {}
        rank = {}
        count = len(M)

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

        for i in range(len(M)):
            for j in range(i + 1, len(M)):
                if M[i][j] == 1:
                    union(i, j)
        return count
