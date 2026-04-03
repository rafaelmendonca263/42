
from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform

if __name__ == "__main__":
    print("\n=== DataDeck Tournament Platform ===")

    print("Registering Tournament Cards...")

    platform = TournamentPlatform()

    dragon = TournamentCard("Fire Dragon",
                            cost=5, rarity="Legendary", rating=1200)
    wizard = TournamentCard("Ice Wizard", cost=4, rarity="Rare", rating=1150)

    dragon_id = "dragon_001"
    wizard_id = "wizard_001"

    platform.cards[dragon_id] = dragon
    platform.cards[wizard_id] = wizard

    for card_id, card in platform.cards.items():
        stats = card.get_tournament_stats()
        print(f"{stats['name']} (ID: {card_id}):")
        print(" - Interfaces: [Card, Combatable, Rankable]")
        print(f" - Rating: {stats['rating']}")
        print(f" - Record: {stats['record']}")

    print("Creating tournament match...")
    match_result = platform.create_match(dragon_id, wizard_id)
    print("Match result:", match_result)

    print("Tournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for line in leaderboard:
        print(line)

    print("Platform Report:")
    report = platform.generate_tournament_report()
    print(report)

    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")
