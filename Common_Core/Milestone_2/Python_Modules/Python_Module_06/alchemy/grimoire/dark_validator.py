from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    spellbook = dark_spell_allowed_ingredients()
    ingredients_lower = ingredients.lower()

    is_valid = any(
        func.__name__.lower() in ingredients_lower for func in spellbook
    )
    status = "VALID" if is_valid else "INVALID"
    return f"{ingredients}: {status}"
