
from ex0.Card import Card


class CreatureCard(Card):
    def __init__(self, name: str, cost: int,
                 rarity: str, attack: int, health: int):
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def get_card_info(self):
        info = super().get_card_info()
        info.update({"attack": self.attack, "health": self.health})
        return info

    def play(self, game_state: dict) -> dict:
        return {
                "card_played": self.name,
                "mana_used": self.cost,
                "effect": "Creature summoned to battlefield"
                }

    def attack_target(self, target) -> dict:
        target_name = getattr(target, "name", str(target))
        return {
                "attacker": self.name,
                "target": target_name,
                "damage_dealt": self.attack,
                "combat_resolved": True
                }
