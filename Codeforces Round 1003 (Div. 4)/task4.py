import bisect
for _ in range(int(input())):
    a_len, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    b.sort()
    possible = True
    curr = float('-inf')

    for i in range(a_len):
        cand = []
        if a[i] >= curr:
            cand.append(a[i])
        pos = bisect.bisect_left(b, curr + a[i])
        if pos < m:
            cand.append(b[pos] - a[i])
        if not cand:
            possible = False
            break
        chosen = min(cand)
        curr = chosen

    print("YES" if possible else "NO")
