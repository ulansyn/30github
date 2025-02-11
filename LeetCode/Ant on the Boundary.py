class Solution:
    def returnToBoundaryCount(self, nums: List[int]) -> int:
        counter = 0
        sum_of_nums = 0
        for i in nums:
            sum_of_nums += i
            if sum_of_nums == 0:
                counter += 1
        return counter