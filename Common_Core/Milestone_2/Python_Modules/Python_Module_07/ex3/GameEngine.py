
from typing import List, Any, Dict, Optional
from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self):
        self.factory: Optional[CardFactory] = None
        self.strategy: Optional[GameStrategy] = None
        self.turns_simulated: int = 0
        self.total_damage: int = 0
        self.cards_created: int = 0

    def simulate_turn(self) -> Dict[str, Any]:
        assert self.factory is not None
        assert self.strategy is not None

        hand = [
            self.factory.create_creature(),
            self.factory.create_creature(),
            self.factory.create_spell(),
        ]

        battlefield: List[Any] = []

        result = self.strategy.execute_turn(hand, battlefield)

        self.turns_simulated += 1
        self.total_damage += result["damage_dealt"]
        self.cards_created += len(hand)

        return result

    def configure_engine(self,
                         factory: CardFactory,
                         strategy: GameStrategy) -> None:
        self.factory = factory
        self.strategy = strategy

    def get_engine_status(self) -> Dict[str, Any]:
        assert self.strategy is not None
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created,
        }
