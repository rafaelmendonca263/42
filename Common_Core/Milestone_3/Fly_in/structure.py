
from dataclasses import dataclass
from typing import Optional

@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: str = "normal"
    color: Optional[str] = None
    max_drones: int = 1