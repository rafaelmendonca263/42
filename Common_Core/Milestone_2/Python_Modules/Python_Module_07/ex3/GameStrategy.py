
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class GameStrategy(ABC):

    @abstractmethod
    def execute_turn(self, hand: List, battlefield: List) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        pass

    @abstractmethod
    def prioritize_targets(self, available_targets: List) -> List:
        pass
