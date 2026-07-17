def hidenp(small: str, big: str) -> bool:
    i = 0
    p = 0

    while p <= len(small) - 1 and i <= len(big) - 1:

            if big[i] == small[p]:
                p = p + 1
                i = i + 1
            else:
                i = i + 1

    return p == len(small):


print(hidenp("abc", "a1b2c3"))
print(hidenp("ace", "abcde"))
print(hidenp("aec", "abcde"))