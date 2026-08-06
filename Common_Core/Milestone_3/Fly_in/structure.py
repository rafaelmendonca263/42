"""Módulo de estruturas de dados básicas do projeto Fly-in."""

from dataclasses import dataclass, field
from typing import List, Literal, Optional


@dataclass
class Hub:
    """Representa uma zona/nó no grafo."""

    name: str
    x: int
    y: int
    hub_type: str = "normal"  # "start", "end" ou "normal"
    color: Optional[str] = None
    max_drones: int = 1
    zone_type: Literal["normal", "restricted", "priority", "blocked"] = "normal"


@dataclass
class Connection:
    """Representa uma ligação bidirecional entre duas zonas."""

    from_hub: str
    to_hub: str
    max_drones: int = 1

    # Aliases com @property para garantir compatibilidade total se usares u/v/max_link_capacity
    @property
    def u(self) -> str:
        return self.from_hub

    @property
    def v(self) -> str:
        return self.to_hub

    @property
    def max_link_capacity(self) -> int:
        return self.max_drones

    @max_link_capacity.setter
    def max_link_capacity(self, value: int) -> None:
        self.max_drones = value


@dataclass
class Drone:
    """Representa um drone e o seu plano de rota."""

    id_num: int
    current_hub: str
    path: List[str] = field(default_factory=list)
