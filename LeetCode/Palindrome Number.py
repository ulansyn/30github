class Solution:
    def isPalindrome(self, x: int) -> bool:
        x_temp = x
        answer = 0
        while x_temp > 0:
            answer = answer * 10 + x_temp % 10
            x_temp //= 10
        return answer == x