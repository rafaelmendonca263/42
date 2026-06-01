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
    hub1: str
    hub2: str
    max_link_capacity: int = 1


class Drone:
    def __init__(self, id_num: int, start_hub: str):
        self.id = f"D{id_num}"
        self.current_hub = start_hub
        self.path = []
        self.steps_to_arrive = 0