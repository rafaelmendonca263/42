def string_sculptor(text: str) -> str:
    text = text.lower()
    upper_flag = False
    res = ""
    for char in text:
        if char in "abcdefghijklmnopqrstuvwxyz":
            if upper_flag is False:
                letra = char.lower()
                upper_flag = True
            else:
                letra = char.upper()
                upper_flag = False
            res += letra
        else:
            res += char

    return res


print(string_sculptor("hello"))
print(string_sculptor("Hello World"))
