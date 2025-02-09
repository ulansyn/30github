t = int(input())
for _ in range(t):
    a_len, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    b = b[0]

    if a_len <= 1:
        print("YES")
        continue

    dp0 = True
    dp1 = True
    last0 = a[0]
    last1 = b - a[0]

    for i in range(1, a_len):
        cand0 = a[i]
        cand1 = b - a[i]
        new_dp0 = False
        new_dp1 = False
        if (dp0 and last0 <= cand0) or (dp1 and last1 <= cand0):
            new_dp0 = True
        if (dp0 and last0 <= cand1) or (dp1 and last1 <= cand1):
            new_dp1 = True
        dp0, dp1 = new_dp0, new_dp1
        if not dp0 and not dp1:
            break
        last0, last1 = cand0, cand1
    print("YES" if dp0 or dp1 else "NO")

