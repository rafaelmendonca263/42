
from ex2.EliteCard import EliteCard


if __name__ == "__main__":

    print("\n=== DataDeck Ability System ===")

    print("\nEliteCard capabilities:")

    card = EliteCard(
        "Arcane Warrior",
        3,              # cost
        "Legendary",    # rarity
        4,              # mana
        4,              # spell_power
        5,              # attack_power
        3               # defense_power
    )

    print("- Card:", ["play", "get_card_info", "is_playable"])
    print("- Combatable:", ["attack", "defend", "get_combat_stats"])
    print("- Magical:", ["cast_spell", "channel_mana", "get_magic_stats"])

    print("\nPlaying Arcane Warrior (Elite Card):")

    print("\nCombat phase:")
    print(f"Attack result: {card.attack('Enemy')}")
    print(f"Defense result: {card.defend(5)}")

    print("\nMagic phase:")
    print(f"Spell cast: {card.cast_spell('Fireball', ['Enemy1', 'Enemy2'])}")
    print(f"Mana channelled: {card.channel_mana(2)}")

    print("\nMultiple interface implementation successful!")
