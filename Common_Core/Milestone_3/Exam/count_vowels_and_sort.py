
def contar_vogais(word):
    word = word.lower()
    count = 0
    for letra in word:
        if letra in 'aeiou':
            count += 1
    return count


def criterios_ordenacao(word):
    return (-contar_vogais(word), word)


def count_vowels_and_sort(words):
    lista_ordenada = sorted(words, key=criterios_ordenacao)
    return lista_ordenada


print(count_vowels_and_sort(["banana", "maca", "abacaxi", "kiwi"]))
# "abacaxi" tem 4 vogais
# "banana" tem 3 vogais
# "maca" tem 2 vogais (empata com "kiwi", mas "maca" vem primeiro no alfabeto)
# "kiwi" tem 2 vogais
# Deve retornar: ['abacaxi', 'banana', 'maca', 'kiwi']
