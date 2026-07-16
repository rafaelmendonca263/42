def whisper_cipher(text: str, shift: int) -> str:
    res = ""
    if shift < 0:
        shift = shift + 26
    for char in text:
        if char.lower() in "abcdefghijklmnopqrstuvwxyz":
            if ord(char.lower()) + shift > ord("z"):
                tmp = (shift - (ord("z") - ord(char.lower()))) + ord("a") - 1
            else:
                tmp = ord(char) + shift

            res += chr(tmp)
        else:
            res += char

    return res


print(whisper_cipher("Hello", 3))
print(whisper_cipher("Hello World!", 1))
print(whisper_cipher("xyz", 3))
print(whisper_cipher("ABC123def", 5))
print(whisper_cipher("", 10))
print(whisper_cipher("abc", -3))
