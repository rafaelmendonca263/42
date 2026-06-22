def reverse_bits(n: int) -> int:
    res = 0

    for _ in range(8):
        res *= 2
        res += (n % 2)
        n = n // 2
        
    return res

print(reverse_bits(128))