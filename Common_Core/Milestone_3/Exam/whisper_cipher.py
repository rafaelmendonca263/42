
def whisper_cipher(text, shift):
    resultado = ""

    for letra in text:
        if 'a' <= letra <= 'z':
            posicao = (ord(letra) - ord('a') + shift) % 26
            resultado += chr(posicao + ord('a'))

        elif 'A' <= letra <= 'Z':
            posicao = (ord(letra) - ord('A') + shift) % 26
            resultado += chr(posicao + ord('A'))

        else:
            resultado += letra

    return resultado
