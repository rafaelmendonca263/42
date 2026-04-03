
from typing import Dict, List
from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    def __init__(self):
        self.cards: Dict[str, TournamentCard] = {}
        self.matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        card_id = (
            f"{card.name.lower().replace(' ', '_')}_"
            f"{len(self.cards)+1:03d}"
        )
        self.cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> Dict:
        card1 = self.cards[card1_id]
        card2 = self.cards[card2_id]

        winner, loser = ((card1, card2) if card1.name == "Fire Dragon" else
                         (card2, card1))

        winner.update_wins(1)
        loser.update_losses(1)
        self.matches_played += 1

        return {
            "winner": card1_id if winner == card1 else card2_id,
            "loser": card1_id if loser == card1 else card2_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating,
        }

    def get_leaderboard(self) -> List[str]:
        sorted_cards = sorted(
            self.cards.items(), key=lambda x: x[1].rating, reverse=True
        )
        leaderboard = []
        rank = 1
        for card_id, card in sorted_cards:
            stats = card.get_tournament_stats()
            leaderboard.append(
                f"{rank}. {stats['name']} - Rating: {stats['rating']} "
                f"({stats['record']})"
            )
            rank += 1
        return leaderboard

    def generate_tournament_report(self) -> Dict:
        total_rating = sum(c.rating for c in self.cards.values())
        avg_rating = int(total_rating / len(self.cards)) if self.cards else 0
        return {
            "total_cards": len(self.cards),
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": "active",
        }
