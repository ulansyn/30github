class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        first = 0
        second = 0
        diffs = 0
        for i in range(len(s2)):
            if s1[i] != s2[i]:
                diffs += 1
                if diffs > 2:
                    return False
                elif diffs == 1:
                    first = i
                else:
                    second = i
        return s1[first] == s2[second] and s2[first] == s1[second]