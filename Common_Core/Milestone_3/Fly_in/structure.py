from dataclasses import dataclass
from typing import Optional


@dataclass
class Hub:
    name: str
    x: int
    y: int
    hub_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1


@dataclass
class Connection:
    hub1: str
    hub2: str
