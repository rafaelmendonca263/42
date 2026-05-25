from typing import Callable


def light_spell_allowed_ingredients() -> list[Callable[[], str]]:
    from elements import create_fire, create_water
    from alchemy.elements import create_air, create_earth

    return [create_fire, create_air, create_water, create_earth]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire.light_validator import validate_ingredients

    return (
        f"Spell recorded: {spell_name} "
        f"({validate_ingredients(ingredients)})"
    )
