from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class Hub:
    name: str
    x: int
    y: int
    hub_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1
    zone_type: Literal["normal", "restricted", "priority", "blocked"] = "normal"


@dataclass
class Connection:
    from_hub: str
    to_hub: str
    max_drones: int = 1


class Drone:
    pass
