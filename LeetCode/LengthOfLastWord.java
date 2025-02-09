class LengthOfLastWord {
    public int lengthOfLastWord(String s) {
        int answer = 0;
        int lengthOfString = s.length();
        while(lengthOfString != 0 && s.charAt(lengthOfString - 1) == ' ') {
            lengthOfString--;
        }
        while(lengthOfString != 0 && s.charAt(lengthOfString - 1) != ' ') {
            answer++;
            lengthOfString--;
        }
        return answer;
    }
}