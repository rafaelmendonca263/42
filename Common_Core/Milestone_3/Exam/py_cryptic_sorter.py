def criterios(string: str):
    tamanho = len(string)
    ordem_alpha = string.lower()
    num_vogais = sum(1 for letra in string.lower() if letra in "aeiou")
    return (tamanho, ordem_alpha, num_vogais)


def cryptic_sorter(strings: list[str]) -> list[str]:
    lista_ordenada = list(strings)
    j = 0
    i = 0

    while i < len(lista_ordenada):
        j = 0
        while j < len(lista_ordenada) - i - 1:
            if criterios(lista_ordenada[j]) > criterios(lista_ordenada[j + 1]):
                lista_ordenada[j], lista_ordenada[j + 1] = (
                    lista_ordenada[j + 1],
                    lista_ordenada[j],
                )
            j = j + 1
        i = i + 1
    return lista_ordenada


print(cryptic_sorter(["apple", "cat", "banana", "dog", "elephant"]))
print(cryptic_sorter(["aaa", "bbb", "AAA", "BBB"]))
