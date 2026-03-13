
from ex0.Card import Card

class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type
        self.consumed = False

    def play(self, game_state: dict) -> dict:
        if self.consumed:
            return {
                "card": self.name,
                "status": "already_used"
            }

        self.consumed = True

        return {
            "card": self.name,
            "mana_used": self.cost,
            "effect_type": self.effect_type,
            "status": "spell_cast"
        }

    def resolve_effect(self, targets: list) -> dict:
        if not self.consumed:
            return {
                "card": self.name,
                "status": "spell_not_cast"
            }

        return {
            "card": self.name,
            "effect_type": self.effect_type,
            "targets": targets,
            "status": "effect_resolved"
        }