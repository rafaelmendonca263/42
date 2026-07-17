def inter(s1: str, s2: str) -> str:
    res = ""
    for char1 in s1:
        for char2 in s2:
            if char1 == char2:
                if char1 not in res:
                    res += char1

    return res


print(inter("hello", "world"))
print(inter("banana", "band"))
print(inter("abcabc", "bc"))
print(inter("abc", "xyz"))
print(inter("", "abc"))
