
from ex0.Card import Card


class ArtifactCard(Card):
    def __init__(self, name: str, cost: int, rarity: str,
                 durability: int, effect: str):
        super().__init__(name, cost, rarity)
        self.durability = durability
        self.effect = effect
        self.in_play = False
        self.destroyed = False

    def play(self, game_state: dict) -> dict:
        self.in_play = True
        return {
                "card": self.name, "mana_used": self.cost,
                "status": "in_play",
                "effect": self.effect
                }

    def activate_ability(self) -> dict:
        if not self.in_play:
            return {
                "card": self.name,
                "status": "not_in_play"
            }

        if self.destroyed:
            self.in_play = False
            return {
                "card": self.name,
                "status": "artifact_destroyed"
            }

        self.durability -= 1

        if self.durability <= 0:
            self.destroyed = True
            return {
                "card": self.name,
                "effect": self.effect,
                "durability": 0,
                "status": "artifact_destroyed"
            }

        return {
            "card": self.name,
            "effect": self.effect,
            "durability": self.durability,
            "status": "active"
        }
