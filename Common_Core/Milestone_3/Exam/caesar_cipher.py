
def caesar_cipher(text, shift):
    res = ""
    shift = shift % 26
    for letra in text:
        if letra.isalpha():
            if letra.islower():
                if ord(letra) + shift > ord('z'):
                    res += (chr(ord('a') + (shift - (ord('z')
                                                     - ord(letra)) - 1)))
                else:
                    res += chr(ord(letra) + shift)
            else:
                if ord(letra) + shift > ord('Z'):
                    res += (chr(ord('A') + (shift
                                            - (ord('Z') - ord(letra)) - 1)))
                else:
                    res += chr(ord(letra) + shift)
        else:
            res += letra

    return res


# Teste 1: Letras simples sem passar do 'z'
print(caesar_cipher("Abc", 3))
# Output: "Def"

# Teste 2: Letras que dão a volta (wrap-around) no fim do alfabeto
print(caesar_cipher("xyz", 3))
# Output: "abc"

# Teste 3: Mistura de maiúsculas, minúsculas, espaços e pontuação
print(caesar_cipher("Hello, World!", 5))
# Output: "Mjqqt, Btwqi!"

# Teste 4: Deslocamento grande (maior que 26, o % 26 resolve isto)
print(caesar_cipher("abc", 28))
# Output: "cde" (andar 28 posições é o mesmo que andar apenas 2)
