def validate_parentheses(s: str) -> bool:
    para = {')':'(', '}':'{', ']':'['}
    lista = []

    for char in s:
        if char in para.values():
            lista.append(char)
        elif char in para:
            if lista and para[char] == lista[-1]:
                lista.pop()
            else:
                return False

    return len(lista) == 0




lista = [
    '()',                               # lista[1] -> Deve dar True
    '(]',                               # lista[2] -> Deve dar False
    '([)]'                              # lista[3] -> Deve dar False
]

for listas in lista:
    print(validate_parentheses(listas))