
def validate_ingredients(ingredients: str) -> str:
    valid_words = ["fire", "water", "earth", "air"]

    ingredients_lower = ingredients.lower()

    if any(word in ingredients_lower for word in valid_words):
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
