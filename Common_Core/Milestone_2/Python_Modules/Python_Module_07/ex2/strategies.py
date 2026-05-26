from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from ex1 import HealCapability, TransformCapability


class StrategyValidationError(Exception):
    """Exceção lançada quando uma estratégia é aplicada a um alvo inválido."""

    pass


@runtime_checkable
class AttackingCreature(Protocol):

    name: str

    def attack(self) -> str: ...


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: AttackingCreature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: AttackingCreature) -> str:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: AttackingCreature) -> bool:
        return isinstance(creature, AttackingCreature)

    def act(self, creature: AttackingCreature) -> str:
        if not self.is_valid(creature):
            name = getattr(creature, "name", "Unknown")
            raise StrategyValidationError(
                f"Invalid Creature '{name}' for this normal strategy"
            )
        return creature.attack()


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: AttackingCreature) -> bool:
        return isinstance(creature, AttackingCreature) and isinstance(
            creature, TransformCapability
        )

    def act(self, creature: AttackingCreature) -> str:
        if not self.is_valid(creature):
            name = getattr(creature, "name", "Unknown")
            raise StrategyValidationError(
                f"Invalid Creature '{name}' for this aggressive strategy"
            )

        assert isinstance(creature, TransformCapability)

        actions = [creature.transform(), creature.attack(), creature.revert()]
        return "\n".join(actions)


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: AttackingCreature) -> bool:
        return isinstance(creature, AttackingCreature) and isinstance(
            creature, HealCapability
        )

    def act(self, creature: AttackingCreature) -> str:
        if not self.is_valid(creature):
            name = getattr(creature, "name", "Unknown")
            raise StrategyValidationError(
                f"Invalid Creature '{name}' for this defensive strategy"
            )

        assert isinstance(creature, HealCapability)

        actions = [creature.attack(), creature.heal()]
        return "\n".join(actions)
