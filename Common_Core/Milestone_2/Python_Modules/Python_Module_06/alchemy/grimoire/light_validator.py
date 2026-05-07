
def validate_ingredients(ingredients: str) -> str:
    spellbook = ["fire", "water", "earth", "air"]
    ingredients_lower = ingredients.lower()

    is_valid = any(item in ingredients_lower for item in spellbook)

    status = "VALID" if is_valid else "INVALID"
    return f"{ingredients} - {status}"
