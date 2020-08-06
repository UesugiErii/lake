# Leetcode 704
#
# 搜索 nums 中的 target

class Solution:
    def search(self, nums, target):
        # find target in sorted list
        left, right = 0, len(nums) - 1
        while left <= right:
            pivot = left + (right - left) // 2
            if nums[pivot] == target:
                return pivot
            if target < nums[pivot]:
                right = pivot - 1
            else:
                left = pivot + 1
        return -1


# Leetcode 34
#
# 在排序数组中查找元素的第一个和最后一个位置

def binarySearchLeft(nums, target):
    l = 0
    r = len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] >= target:
            r = mid - 1
        else:
            l = mid + 1
    if l < len(nums) and nums[l] == target:
        return l
    return -1


def binarySearchRight(nums, target):
    l = 0
    r = len(nums) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if nums[mid] <= target:
            l = mid + 1
        else:
            r = mid - 1
    if r >= 0 and nums[r] == target:
        return r
    return -1


nums = [5, 7, 7, 8, 8, 10]
target = 8
print(binarySearchLeft(nums, target), binarySearchRight(nums, target))
