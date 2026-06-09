def word_frequency(text):
    dict_split = text.split(" ")
    dict_res = {}
    for word in dict_split:
        word = word.lower()
        if word not in dict_res:
            dict_res[word] = 1
        else:
            dict_res[word] += 1

    return dict_res
