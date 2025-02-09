for i in range(int(input())):
    s = input()
    if len(s) == 1:
        print(1)
    else:
        flag = False
        for j in range(1, len(s)):
            if s[j - 1] == s[j]:
                flag = True
                break
        if flag:
            print(1)
        else:
            print(len(s))