"""Basic data structures module for the Fly-in project."""

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Set, Tuple


@dataclass
class Hub:
    """Represents a zone/node in the simulation graph.

    Attributes:
        name (str): Unique identifier name of the hub.
        x (int): X coordinate on the Cartesian plane for visualization.
        y (int): Y coordinate on the Cartesian plane for visualization.
        hub_type (str): Hub type ("start", "end", or "normal").
        color (Optional[str]): Associated color for graphic rendering.
        max_drones (int): Maximum number of simultaneous drones
        allowed in the hub.
        zone_type (Literal): Special zone type ("normal", "restricted",
            "priority", "blocked").
        drones_inside (Set[int]): Set of drone IDs currently inside this hub.
    """

    name: str
    x: int
    y: int
    hub_type: str = "normal"  # "start", "end", or "normal"
    color: Optional[str] = None
    max_drones: int = 1
    zone_type: Literal["normal", "restricted", "priority", "blocked"] = (
        "normal"
    )
    drones_inside: Set[int] = field(default_factory=set)


@dataclass
class Connection:
    """Represents a bidirectional connection between two zones (hubs).

    Attributes:
        from_hub (str): Name of the source hub.
        to_hub (str): Name of the destination hub.
        max_drones (int): Maximum drone transit capacity on the
            connection per turn.
    """

    from_hub: str
    to_hub: str
    max_drones: int = 1
    drones_inside: Set[int] = field(default_factory=set)

    @property
    def u(self) -> str:
        """Returns the source hub (compatible alias)."""
        return self.from_hub

    @property
    def v(self) -> str:
        """Returns the destination hub (compatible alias)."""
        return self.to_hub

    @property
    def max_link_capacity(self) -> int:
        """Returns the maximum link capacity (compatible alias)."""
        return self.max_drones

    @max_link_capacity.setter
    def max_link_capacity(self, value: int) -> None:
        """Defines the maximum capacity of connection."""
        self.max_drones = value


@dataclass
class Drone:
    """Represents an individual drone and its current state in the simulation.

    Attributes:
        id_num (int): Unique numerical identifier of the drone.
        current_hub (str): Name of the hub where the drone is
        currently located.
        path (List[str]): List of nodes/hubs making up the planned path.
        status (str): Current status of the drone ("waiting", "moving",
            "in_transit", "finished").
        transit_connection (Optional[Tuple[str, str]]): Active connection if
            in transit through a restricted zone.
    """

    id_num: int
    current_hub: str
    path: List[str] = field(default_factory=list)
    status: str = "waiting"  # "waiting", "moving", "in_transit", "finished"
    transit_connection: Optional[Tuple[str, str]] = None
