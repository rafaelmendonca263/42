
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard

if __name__ == "__main__":
    
    creature = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)

    print("\n=== DataDeck Card Foundation ===")

    print("\nTesting Abstract Base Class Design:")

    print("\nCreatureCard Info:")
    print(f"{creature.get_card_info()}\n")

    print("Playing Fire Dragon with 6 mana available:")
    print(f"Playable: {creature.is_playable(6)}")
    print(f"Play result: {creature.play({})}\n")

    print("Fire Dragon attacks Goblin Warrior:")
    print(f"Attack result: {creature.attack_target("Goblin Warrior")}\n")

    print("Testing insufficient mana (3 available):")
    print(f"Playable: {creature.is_playable(3)}\n")

    print("Abstract pattern successfully demonstrated!")