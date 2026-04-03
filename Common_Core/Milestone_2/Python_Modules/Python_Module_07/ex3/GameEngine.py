
from typing import Dict, Any, List
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:

    def __init__(self) -> None:
        self.factory: CardFactory | None = None
        self.strategy: GameStrategy | None = None
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0

    def configure_engine(
        self,
        factory: CardFactory,
        strategy: GameStrategy
    ) -> None:
        self.factory = factory
        self.strategy = strategy

    def _format_hand(self, hand: List) -> List[str]:
        formatted_hand = []
        for card in hand:
            formatted_hand.append(f"{card.name} ({card.cost})")
        return formatted_hand

    def simulate_turn(self) -> Dict[str, Any]:
        hand = [
            self.factory.create_creature(),
            self.factory.create_creature("goblin"),
            self.factory.create_spell(),
        ]

        battlefield = []

        actions = self.strategy.execute_turn(hand, battlefield)

        self.turns_simulated += 1
        self.total_damage += actions["damage_dealt"]
        self.cards_created += len(hand)

        return {
            "hand": self._format_hand(hand),
            "strategy": self.strategy.get_strategy_name(),
            "actions": actions,
        }

    def get_engine_status(self) -> Dict[str, Any]:
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created,
        }
