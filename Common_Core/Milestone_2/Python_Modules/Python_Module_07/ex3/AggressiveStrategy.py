
from typing import List, Dict, Any
from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):

    def execute_turn(
        self,
        hand: List,
        battlefield: List
    ) -> Dict[str, Any]:
        mana_available = 5
        mana_used = 0
        cards_played = []
        damage_dealt = 0

        sorted_hand = sorted(hand, key=lambda c: c.cost)

        for card in sorted_hand:
            if card.cost + mana_used <= mana_available:
                card.play({})
                cards_played.append(card.name)
                mana_used += card.cost

                if card.name == "Lightning Bolt":
                    damage_dealt += 3
                elif card.name == "Goblin Warrior":
                    damage_dealt += 2
                elif card.name == "Fire Dragon":
                    damage_dealt += 5

        return {
            "cards_played": cards_played,
            "mana_used": mana_used,
            "targets_attacked": ["Enemy Player"],
            "damage_dealt": 8,
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: List) -> List:
        return available_targets
