
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):

    def __init__(self):
        self.strategy_name = "AggressiveStrategy"

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        actions = {
            "cards_played": [],
            "mana_used": 0,
            "targets_attacked": [],
            "damage_dealt": 0
        }

        available_mana = 10
        creatures = [card for card in hand if getattr(card, "type", "") == "Creature"]
        spells = [card for card in hand if getattr(card, "type", "") == "Spell"]

        for card in creatures + spells:
            if card.is_playable(available_mana):
                result = card.play({"mana": available_mana})
                available_mana -= result["mana_used"]
                actions["cards_played"].append(result["card_played"])
                actions["mana_used"] += result["mana_used"]

                if getattr(card, "type", "") == "Creature":
                    actions["targets_attacked"].append("Enemy Player")
                    actions["damage_dealt"] += getattr(card, "attack", 0)

        return actions
    
    def simulate_turn(self) -> dict:
        if not self.factory or not self.strategy:
            raise ValueError("Engine not configured with factory and strategy")

        hand = [
            self.factory.create_creature(),
            self.factory.create_creature(),
            self.factory.create_spell()
        ]
        battlefield = []

        actions = self.strategy.execute_turn(hand, battlefield)
        return actions

    def get_strategy_name(self) -> str:
        return self.strategy_name

    def prioritize_targets(self, available_targets: list) -> list:
        return sorted(
            available_targets,
            key=lambda t: getattr(t, "attack", 0),
            reverse=True
        )
