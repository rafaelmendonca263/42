
from alchemy.grimoire import validate_ingredients, record_spell

if __name__ == "__main__":

    print("\n=== Circular Curse Breaking ===")

    print("\nTesting ingredient validation:")
    print("validate_ingredients(\"fire air\"): "
          f"{validate_ingredients("fire air")}")
    print("validate_ingredients(\"dragon scales\"): "
          f"{validate_ingredients("dragon scales")}")

    print("\nTesting spell recording with validation:")
    print(f"record_spell(\"Fireball\", \"fire air\"): "
          f"{record_spell('Fireball', 'fire air')}")
    print(f"record_spell(\"Dark Magic\", \"shadow\"): "
          f"{record_spell('Dark Magic', 'shadow')}")

    print("Circular dependency curse avoided using late imports!")
    print("All spells processed safely!")
