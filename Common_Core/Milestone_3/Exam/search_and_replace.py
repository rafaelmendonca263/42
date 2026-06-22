def search_and_replace(text: str, search: str, replace: str) -> str:
    res = ""
    
    if len(search) != 1 or len(replace) != 1:
        return text
        
    for letra in text:
        if letra == search:
            res += replace
        else:
            res += letra

    return res

print(search_and_replace("a a a", " ", "?"))