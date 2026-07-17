def pattern_tracker(text: str) -> int:
    i = 0
    count = 0
    while i <= len(text) - 2:
        try:
            nmb1 = int(text[i])
            nmb2 = int(text[i + 1])
        except Exception:
            i = i + 1
            continue

        if nmb2 == nmb1 + 1:
            if nmb1 != 9:
                count += 1
        i = i + 1

    return count


print(pattern_tracker("123"))
print(pattern_tracker("12a34"))
print(pattern_tracker("987654321"))
print(pattern_tracker("01234567"))
print(pattern_tracker("abc"))
print(pattern_tracker("1a2b3c4"))
print(pattern_tracker("112233"))
