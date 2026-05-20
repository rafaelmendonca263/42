from abc import ABC, abstractmethod


class Creature(ABC):
    name: str
    type: str

    def __init__(self, name: str, element_type: str) -> None:
        self.name: str = name
        self.element_type: str = element_type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.element_type} type Creature"
