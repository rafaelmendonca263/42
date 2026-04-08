
from typing import Dict, Any
from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        rating: int = 1200
    ):
        super().__init__(name, cost, rarity)
        self.attack_power = 5
        self.health = 5
        self.rating = rating
        self.wins = 0
        self.losses = 0
        self.record = f"{self.wins}-{self.losses}"

    def play(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
        }

    def attack(self, target: str) -> Dict[str, Any]:
        return {
            "attacker": self.name,
            "target": target,
            "damage_dealt": self.attack,
            "combat_resolved": True,
        }

    def defend(self, incoming_damage: int) -> Dict[str, Any]:
        blocked = min(2, incoming_damage)
        damage_taken = incoming_damage - blocked
        return {
            "defender": self.name,
            "damage_taken": damage_taken,
            "damage_blocked": blocked,
            "still_alive": True,
        }

    def get_combat_stats(self) -> Dict[str, Any]:
        return {
            "attack": self.attack,
            "health": self.health,
        }

    def calculate_rating(self) -> int:
        return self.rating + (16 * self.wins) - (16 * self.losses)

    def update_wins(self, wins: int) -> None:
        self.wins += wins
        self.record = f"{self.wins}-{self.losses}"

    def update_losses(self, losses: int) -> None:
        self.losses += losses
        self.record = f"{self.wins}-{self.losses}"

    def get_rank_info(self) -> Dict[str, Any]:
        return {
            "rating": self.calculate_rating(),
            "wins": self.wins,
            "losses": self.losses,
            "record": self.record,
        }

    def get_tournament_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "rating": self.calculate_rating(),
            "record": self.record,
        }
