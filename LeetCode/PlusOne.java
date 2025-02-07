class PlusOne {
    public int[] plusOne(int[] digits) {
        Boolean memory = false;
        Boolean isNewArray = false;
        for(int i = digits.length - 1; i >= 0; i--) {
            if(digits[i] == 9) {
                digits[i] = 0;
                memory = true;
                if(i == 0){
                    isNewArray = true;
                }
            } else {
                digits[i] += 1;
                memory = false;
                return digits;
            }
        }
        if(isNewArray) {
            int[] newArray = new int[digits.length + 1];
            newArray[0] = 1;
            for(int i = 1; i < digits.length + 1; i++) {
                newArray[i] = digits[i - 1];
            }
            return newArray;
        }
        return digits;
    }
}