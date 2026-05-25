from abc import ABC, abstractmethod
from ex0 import Creature
from ex1 import HealCapability, TransformCapability


class StrategyValidationError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> str:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise StrategyValidationError(
                f"Invalid Creature '{creature.name}' for this normal strategy"
            )
        return creature.attack()


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise StrategyValidationError(
                f"Invalid Creature '{creature.name}' for this "
                "aggressive strategy"
            )
        assert isinstance(creature, TransformCapability)

        actions = [creature.transform(), creature.attack(), creature.revert()]
        return "\n".join(actions)


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise StrategyValidationError(
                f"Invalid Creature '{creature.name}' for this "
                "defensive strategy"
            )
        assert isinstance(creature, HealCapability)

        actions = [creature.attack(), creature.heal()]
        return "\n".join(actions)
