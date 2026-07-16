def bracket_validator(s: str) -> bool:
    para = {"}": "{", ")": "(", "]": "["}
    lista = []

    for char in s:
        if char in para.values():
            lista.append(char)
        elif char in para:
            if para[char] == lista[-1]:
                lista.pop(-1)

    return len(lista) == 0


print(bracket_validator("()"))  # True
print(bracket_validator("()[]{}"))  # True
print(bracket_validator("(]"))  # False
