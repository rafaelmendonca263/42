def is_palindrome(text):
    text_clean = text.lower()
    return text_clean == text_clean[::-1]
