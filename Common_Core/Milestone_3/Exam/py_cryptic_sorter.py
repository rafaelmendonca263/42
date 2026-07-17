def helper(string: str):
    tamanho = len(string)
    ascii_ord = string.lower()
    count = 0
    for char in string:
        if char in "aeiou":
            count += 1

    return (tamanho, ascii_ord, count, string)


def cryptic_sorter(strings: list[str]) -> list[str]:
    i = 0
    j = 0
    res = strings

    while i < len(res) - 1:
        j = 0
        while j < len(res) - 1 - i:
            if helper(res[j]) > helper(res[j + 1]):
                tmp = res[j]
                res[j] = res[j + 1]
                res[j + 1] = tmp
            j = j + 1
        i = i + 1

    return res
