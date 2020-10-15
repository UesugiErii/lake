# Leetcode 758
#
# 给定一个关键词集合 words 和一个字符串 S，将所有 S 中出现的关键词加粗
# 所有在标签 <b> 和 </b> 中的字母都会加粗
#
# 返回的字符串需要使用尽可能少的标签，当然标签应形成有效的组合
#
# 例如，给定 words = ["ab", "bc"] 和 S = "aabcd"，需要返回 "a<b>abc</b>d"
# 注意返回 "a<b>a<b>b</b>c</b>d" 会使用更多的标签，因此是错误的

from typing import List


# 定义一个字典树
class Trie:
    def __init__(self):
        self.trie = {}

    def insert(self, word):
        node = self.trie
        for w in word:
            if w not in node:
                node[w] = {}
            node = node[w]
        node["#"] = 1


class Solution:
    def boldWords(self, words: List[str], S: str) -> str:
        trie = Trie()
        for word in words:
            trie.insert(word)

        # 获取所有可以插入标签的点坐标
        def get_location(location: List[List[int]]) -> List[List[int]]:
            for i in range(len(S)):
                temp = trie.trie
                if S[i] in temp:
                    start = i
                    for j in range(i, len(S)):
                        if S[j] in temp:
                            temp = temp[S[j]]
                            if "#" in temp.keys():
                                location.append([start, j + 1])
                        else:
                            break
            return location

        # 合并区间 Leetcode 56
        def merge(intervals: List[List[int]]) -> List[List[int]]:
            intervals.sort(key=lambda x: [x[0], x[1]])
            res = []
            if len(intervals) == 0:
                return res
            start = intervals[0][0]
            end = intervals[0][1]
            for i in range(1, len(intervals)):
                if intervals[i][0] <= end:
                    if intervals[i][1] > end:
                        end = intervals[i][1]
                else:
                    res.append([start, end])
                    start = intervals[i][0]
                    end = intervals[i][1]
            res.append([start, end])
            return res

        # 插入标签
        def insert_label(location: List[List[int]], string: str) -> str:
            res = ""
            head = 0
            for loc in location:
                res += string[head:loc[0]] + "<b>" + string[loc[0]:loc[1]] + "</b>"
                head = loc[1]
            res += string[head:]
            return res

        return insert_label(merge(get_location([])), S)
