class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        
        bit_count = [0] * 32
        
        for num in nums:
            for i in range(32):
                bit_count[i] += (num >> i) & 1
        result = 0
        for i in range(32):
            if bit_count[i] % 3 != 0:
                if i == 31:
                    result -= (1 << i)
                else:
                    result |= (1 << i)
        
        return result