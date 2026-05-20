from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyException(Exception):
    pass


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
        return True

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
            raise InvalidStrategyException(
                f"Invalid Creature '{creature.name}' for this "
                "aggressive strategy"
            )

        if isinstance(creature, TransformCapability):
            res_trans = creature.transform()
            res_att = creature.attack()
            res_revert = creature.revert()
            return f"{res_trans}\n{res_att}\n{res_revert}"

        return ""


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> str:
        if not self.is_valid(creature):
            raise InvalidStrategyException(
                f"Invalid Creature '{creature.name}' for this "
                "defensive strategy"
            )

        if isinstance(creature, HealCapability):
            res_att = creature.attack()
            res_heal = creature.heal()
            return f"{res_att}\n{res_heal}"

        return ""
