class Solution {
    public int climbStairs(int n) {
        if (n < 4) return n;
        int previous1 = 3;
        int previous2 = 2;
        int current = 0;
        for (int i = 3; i < n; i++) {
            current = previous1 + previous2;
            previous2 = previous1;
            previous1 = current;
        }
        return current;
    }
}
