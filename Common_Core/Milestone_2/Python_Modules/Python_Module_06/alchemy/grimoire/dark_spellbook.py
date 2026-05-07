from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients():
    from elements import create_fire, create_water
    from alchemy.elements import create_air, create_earth

    return [create_fire, create_air, create_water, create_earth]


def dark_spell_record(spell_name: str, ingredients: str):

    return (
        f"Spell recorded: {spell_name} "
        f"({validate_ingredients(ingredients)})"
    )
