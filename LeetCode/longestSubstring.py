def length_of_longest_substring(s): max_length = 0 start = 0 seen = {}

for end in range(len(s)):
    if s[end] in seen and seen[s[end]] >= start:
        start = seen[s[end]] + 1

    seen[s[end]] = end
    max_length = max(max_length, end - start + 1)

return max_length

Пример использования

s = "abcabcbb" print(length_of_longest_substring(s))

