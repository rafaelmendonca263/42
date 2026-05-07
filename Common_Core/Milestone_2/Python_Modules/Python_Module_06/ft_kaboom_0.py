
from alchemy import grimoire


if __name__ == "__main__":
    print("=== Kaboom 0 ===")
    print("Access to alchemy/grimoire directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    print("Testing record light spell: "
          f"{grimoire.light_spell_record('Fantasy', 'Earth, wind and fire')}")
