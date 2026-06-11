def alternate_case(s):
    res = ""
    big = True
    for char in s:
        if char.isalpha():
            if big:
                res += char.upper()
                big = False
            else:
                res += char.lower()
                big = True
        else:
            res += char
    return res
