
def is_anagram(str1, str2):
    return (sorted(str1.replace(" ", "").lower()) ==
            sorted(str2.replace(" ", "").lower()))


print(is_anagram("Listen", "Silent"))
# Deve retornar: True (ignorando maiúsculas)

print(is_anagram("O galo", "A gola"))
# Deve retornar: False (letras diferentes: 'o'/'a')

print(is_anagram("Tom Marvolo Riddle", "I am Lord Voldemort"))
# Deve retornar: True (se ignorares os espaços e as maiúsculas!)
