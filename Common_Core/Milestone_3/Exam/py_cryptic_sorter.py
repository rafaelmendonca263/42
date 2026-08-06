def helper(string: str):
    tamanho = len(string)
    ascii_ord = string.lower()

    return (tamanho, ascii_ord)


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


print(cryptic_sorter(['aaa', 'bbb', 'AAA', 'BBB']))
