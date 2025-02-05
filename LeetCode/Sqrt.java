class Sqrt {
    public int mySqrt(int x) {
        if(x == 1 || x == 0) return x;
        int result = 0;
        int left = 0;
        int right = x;
        while(left <= right) {
            int middle = left + (right - left) / 2;
            if ((long) middle * middle <= x) {
                result = middle;
                left = middle + 1;
            } else {
                right = middle - 1;
            }
        }
        return result;
    }
}