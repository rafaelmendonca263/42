from typing import Any, Dict, List, Optional, Union
from structure import Connection, Hub, Drone
from reservation import ReservationTable
from pathfinder import SpaceTimeAStar

COLOR_MAP: Dict[str, str] = {
    # Colors ANSI
    "black": "\033[30m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "purple": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "gray": "\033[90m",
    "grey": "\033[90m",
    # Expanded colors (ANSI 256)
    "orange": "\033[38;5;208m",
    "pink": "\033[38;5;205m",
    "brown": "\033[38;5;130m",
    "gold": "\033[38;5;220m",
    "lime": "\033[38;5;118m",
    "teal": "\033[38;5;37m",
    "navy": "\033[38;5;19m",
    "violet": "\033[38;5;135m",
    "indigo": "\033[38;5;54m",
    "reset": "\033[0m",
}


def get_ansi_color(color_name: Optional[str]) -> str:
    """Converts the name of a color to its corresponding ANSI sequence.
    If the color is unknown, it uses a deterministic hash to generate a
    unique color from the ANSI spectrum of 256 colors.
    """
    if not color_name or color_name.lower() in ("none", "null"):
        return ""

    color_key = color_name.lower().strip()
    if color_key in COLOR_MAP:
        return COLOR_MAP[color_key]

    # Deterministic fallback for any string of arbitrary color
    color_code = (abs(hash(color_key)) % 216) + 16
    return f"\033[38;5;{color_code}m"


class Simulation:
    """Manages the overall drone routing simulation, executing turns,
    tracking drone states, handling reservation updates, and
    managing visualization.
    """

    def __init__(
        self,
        parsed_data: Dict[str, Any],
        visual: bool = False,
    ) -> None:
        """Initializes the simulation engine with parsed map data and
        configuration parameters.
        """
        self.hubs_list: List[Hub] = parsed_data["hubs"]
        self.raw_connections: List[Union[Connection, str]] = parsed_data[
            "connections"
        ]
        self.nb_drones: int = parsed_data["nb_drones"]
        self.start_hub: str = parsed_data["start_hub"]
        self.end_hub: str = parsed_data["end_hub"]
        self.visual = visual

        # O(1) Hub mapping
        self.hubs: Dict[str, Hub] = {h.name: h for h in self.hubs_list}
        self.connections: Dict[str, Connection] = {}
        self.adj: Dict[str, List[str]] = {}

        # Connection mapping
        for conn_item in self.raw_connections:
            if isinstance(conn_item, Connection):
                u, v = conn_item.from_hub, conn_item.to_hub
                conn_obj = conn_item
            elif isinstance(conn_item, str):
                parts = (
                    conn_item.split("-")
                    if "-" in conn_item
                    else conn_item.split()
                )
                if len(parts) >= 2:
                    u, v = parts[0].strip(), parts[1].strip()
                    conn_obj = Connection(from_hub=u, to_hub=v)
                else:
                    continue
            else:
                continue

            link_key = "-".join(sorted([u, v]))
            self.connections[link_key] = conn_obj
            self.adj.setdefault(u, []).append(v)
            self.adj.setdefault(v, []).append(u)

        self.current_turn: int = 0
        self.output_turns: List[List[str]] = []
        self.reservation_table = ReservationTable()
        self.pathfinder = SpaceTimeAStar(
            self.hubs, self.connections, self.adj, self.reservation_table
        )

        # Drone initialization
        self.drones: List[Drone] = []
        self.drone_states: Dict[int, Dict[str, Any]] = {}

        start_hub_obj = self.hubs.get(self.start_hub)

        for i in range(1, self.nb_drones + 1):
            schedule = self.pathfinder.find_schedule(
                self.start_hub, self.end_hub, start_turn=1
            )

            if schedule:
                self.pathfinder.commit_schedule(schedule, self.end_hub)

            path_nodes = [node for node, _ in schedule]
            drone_obj = Drone(
                id_num=i, current_hub=self.start_hub, path=path_nodes
            )
            drone_obj.transit_connection = None
            self.drones.append(drone_obj)

            # Register initial drones inside the start hub
            if start_hub_obj:
                start_hub_obj.drones_inside.add(i)

            self.drone_states[i] = {
                "schedule": schedule,
                "schedule_idx": 0,
                "status": "waiting",
                "in_transit_to": None,
            }

        self.visualizer = None
        if self.visual:
            try:
                from visualizer import DroneVisualizer

                self.visualizer = DroneVisualizer(self)
            except ImportError:
                self.visual = False

    def is_finished(self) -> bool:
        """Checks if all drones have successfully reached the end hub."""
        return all(
            st["status"] == "finished" for st in self.drone_states.values()
        )

    def _format_move(self, drone_id: int, target: str) -> str:
        """Formats a move string for a specific drone and target node."""
        return f"D{drone_id}-{target}"

    def run_turn(self) -> List[str]:
        """Executes a single simulation turn, processing movements."""
        self.current_turn += 1
        turn_moves: List[str] = []

        for drone in self.drones:
            st = self.drone_states[drone.id_num]

            if st["status"] == "finished":
                continue

            if st["status"] == "in_transit":
                old_conn_key = (
                    "-".join(sorted(drone.transit_connection))
                    if drone.transit_connection
                    else None
                )
                if old_conn_key and old_conn_key in self.connections:
                    conn = self.connections[old_conn_key]
                    conn.drones_inside.discard(drone.id_num)

                target_hub = st["in_transit_to"]
                st["in_transit_to"] = None

                target_hub_obj = self.hubs.get(target_hub)
                if target_hub_obj:
                    target_hub_obj.drones_inside.add(drone.id_num)

                drone.current_hub = target_hub
                drone.transit_connection = None
                st["status"] = (
                    "finished" if target_hub == self.end_hub else "moving"
                )
                turn_moves.append(self._format_move(drone.id_num, target_hub))
                continue

            schedule = st["schedule"]
            idx = st["schedule_idx"]

            if not schedule or idx >= len(schedule) - 1:
                continue

            curr_hub, curr_t = schedule[idx]
            next_hub, _ = schedule[idx + 1]

            if self.current_turn == curr_t:
                st["schedule_idx"] += 1

                if curr_hub == next_hub:
                    continue

                curr_hub_obj = self.hubs.get(curr_hub)
                if curr_hub_obj:
                    curr_hub_obj.drones_inside.discard(drone.id_num)

                next_hub_obj = self.hubs.get(next_hub)
                zone_type = (
                    next_hub_obj.zone_type if next_hub_obj else "normal"
                )

                if zone_type == "restricted" and next_hub != self.end_hub:
                    st["status"] = "in_transit"
                    st["in_transit_to"] = next_hub
                    drone.transit_connection = (curr_hub, next_hub)
                    conn_name = f"{curr_hub}-{next_hub}"

                    conn_key = "-".join(sorted([curr_hub, next_hub]))
                    if conn_key in self.connections:
                        conn = self.connections[conn_key]
                        conn.drones_inside.add(drone.id_num)

                    turn_moves.append(
                        self._format_move(drone.id_num, conn_name)
                    )
                else:
                    if next_hub_obj:
                        next_hub_obj.drones_inside.add(drone.id_num)

                    drone.current_hub = next_hub
                    drone.transit_connection = None
                    st["status"] = (
                        "finished" if next_hub == self.end_hub else "moving"
                    )
                    turn_moves.append(
                        self._format_move(drone.id_num, next_hub)
                    )

        return turn_moves

    def run(self) -> None:
        """Runs the complete simulation loop until all drones
        reach destination.
        Handles visualization updates and full ANSI colored turn printing.
        """
        reset_code = COLOR_MAP["reset"]

        while not self.is_finished():
            moves = self.run_turn()
            if moves:
                self.output_turns.append(moves)

                # Building the line with dynamic colors for the terminal
                colored_moves: List[str] = []
                for move in moves:
                    target = move.split("-", 1)[1]
                    element: Any = self.hubs.get(target)

                    if not element and "-" in target:
                        parts = target.split("-")
                        if len(parts) == 2:
                            conn_key = "-".join(sorted(parts))
                            element = self.connections.get(conn_key)

                    color_code = ""

                    if element:
                        if hasattr(element, "color") and element.color:
                            color_code = get_ansi_color(str(element.color))

                        if not color_code and hasattr(element, "zone_type"):
                            zt = element.zone_type
                            if zt == "restricted":
                                color_code = COLOR_MAP["orange"]
                            elif zt == "priority":
                                color_code = COLOR_MAP["gold"]
                            elif zt == "blocked":
                                color_code = COLOR_MAP["gray"]

                    if not color_code:
                        color_code = COLOR_MAP["cyan"]

                    colored_moves.append(f"{color_code}{move}{reset_code}")

                print(" ".join(colored_moves))

            if self.visualizer:
                self.visualizer.update(self.drones, self.current_turn)

            if not moves and not self.is_finished():
                if any(
                    st["status"] == "in_transit"
                    for st in self.drone_states.values()
                ):
                    continue
                err_msg = (
                    f"{COLOR_MAP['red']}❌ Simulation error: "
                    f"Deadlock detected.{reset_code}"
                )
                print(err_msg)
                break
