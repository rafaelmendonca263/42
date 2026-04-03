from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck
from tools.card_generator import CardGenerator

if __name__ == "__main__":

    generator = CardGenerator()
    creature_data = generator.get_creature("Fire Dragon")
    spell_data = generator.get_spell("Lightning Bolt")
    artifact_data = generator.get_artifact("Mana Crystal")

    creature = CreatureCard(creature_data['name'], creature_data['cost'],
                            creature_data['rarity'], creature_data['attack'],
                            creature_data['health'])

    spell = SpellCard(spell_data['name'], spell_data['cost'],
                      spell_data['rarity'], spell_data['effect_type'])

    artifact = ArtifactCard(artifact_data['name'], artifact_data['cost'],
                            artifact_data['rarity'],
                            artifact_data['durability'],
                            artifact_data['effect'])

    deck = Deck()

    print("\n=== DataDeck Deck Builder ===")
    print("\nBuilding deck with different card types...")

    deck.add_card(creature)
    deck.add_card(spell)
    deck.add_card(artifact)

    print(f"Deck stats: {deck.get_deck_stats()}\n")

    deck.shuffle()

    print("Drawing and playing cards:\n")

    while True:
        card = deck.draw_card()
        if card is None:
            break

        print(f"Drew: {card.name} ({type(card).__name__.replace('Card', '')})")
        result = card.play({})
        print(f"Play result: {result}\n")

    print("Polymorphism in action: Same interface, different card behaviors!")
