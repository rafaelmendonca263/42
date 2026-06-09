
def validate_parentheses(s):
    lista = []
    dict = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in dict.values():
            lista.append(char)
        elif char in dict:
            if not lista:
                return False
            if lista[-1] != dict[char]:
                return False
            lista.pop()

    return len(lista) == 0


"""
lista = '{{{{{{{[[[[[[(())]]]]]]}}}}}}}'
print(validate_parentheses(lista))
 """
