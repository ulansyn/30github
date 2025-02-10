class ClearDigits {
    public String clearDigits(String s) {
        List<Character> stack = new ArrayList<>();
        for(char i: s.toCharArray()) {
            if(!Character.isDigit(i)) {
                stack.add(i);
            } else {
                stack.remove(stack.size() - 1);
            }
        }
        StringBuilder result = new StringBuilder("");
        for(char i: stack) {
            result.append(i);
        }
        return result.toString();
    }
}