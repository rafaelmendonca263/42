
def find_longest_word(text):
    dict = {}
    maior_palavra = ""

    if text == "":
        return ""

    text_split = text.split(" ")
    for word in text_split:
        for _ in word:
            dict[word] = len(word)
        if len(word) > len(maior_palavra):
            maior_palavra = word

    return maior_palavra
