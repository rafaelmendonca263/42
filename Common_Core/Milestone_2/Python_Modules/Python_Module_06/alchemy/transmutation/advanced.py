
from .basic import lead_to_gold
from ..potions import healing_potion


def philosophers_stone():

    lead_to_gold_result = lead_to_gold()
    healing_potion_result = healing_potion()

    return (
        f"Philosopher’s stone created using {lead_to_gold_result} "
        f"and {healing_potion_result}"
    )


def elixir_of_life():
    return "Elixir of life: eternal youth achieved!"
