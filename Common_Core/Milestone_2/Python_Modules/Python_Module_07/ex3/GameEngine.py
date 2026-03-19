
from ex3.GameStrategy import GameStrategy
from ex3.CardFactory import CardFactory


class GameEngine():
    def __init__(self):
        self.factory = None
        self.strategy = None
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

    def simulate_turn(self) -> dict:
        creature = self.factory.create_creature()
        spell = self.factory.create_spell()
        artifact = self.factory.create_artifact()

        hand = [creature, spell, artifact]
        battlefield = []

        actions = self.strategy.execute_turn(hand, battlefield)

        turn_report = {
            "turns_simulated": 1,
            "strategy": self.strategy.get_strategy_name(),  # ✅ nome da strategy
            "total_damage": actions.get("damage_dealt", 0),
            "cards_created": len(hand),
            "actions": actions
        }

        return turn_report

    def get_engine_status(self) -> dict:
        return {
            "factory": self.factory.__class__.__name__,
            "strategy": self.strategy.get_strategy_name(),
            "available_types": self.factory.get_supported_types()
        }
