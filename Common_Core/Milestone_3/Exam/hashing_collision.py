def hashing_collision(strings: list[str]) -> dict[int, list[str]]:
    res = {}

    for frase in strings:
        temp = 0
        for letra in frase:
            temp += ord(letra)
        
        if temp in res:
            res[temp].append(frase)
        else:
            res[temp] = [frase]
    
    return res

print(hashing_collision(["abc", "cba", "a", "b"]))