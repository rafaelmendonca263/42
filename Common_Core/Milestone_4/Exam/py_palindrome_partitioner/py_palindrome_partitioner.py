def palindrome_partitioner(s: str) -> int:
    if not s or is_palindrome(s):
        return 0
    
    min_cuts = len(s) - 1

    for i in range(1, len(s)):
        prefix = s[:i]
        if prefix == prefix[::-1]:
            cuts = 1 + palindrome_partitioner(s[i:])
            if cuts < min_cuts:
                min_cuts = cuts

    return min_cuts

print(palindrome_partitioner("aab"))  # Expected: 1
print(palindrome_partitioner("aba"))  # Expected: 0
print(palindrome_partitioner("abc"))  # Expected: 2