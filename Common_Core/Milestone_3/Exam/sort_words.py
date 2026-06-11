
def criterios(palavra):
    com = len(palavra)
    vogais = 0
    for letra in palavra.lower():
        if letra in "aeiou":
            vogais += 1
    return (com, vogais, palavra)


def sort_words(word_list):

    return sorted(word_list, key=criterios)
