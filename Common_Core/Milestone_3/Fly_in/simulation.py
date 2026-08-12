from typing import Any, Dict, List, Union
from structure import Connection, Hub, Drone
from reservation import ReservationTable
from pathfinder import SpaceTimeAStar


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

        Args:
            parsed_data (Dict[str, Any]): Dictionary containing parsed
            hubs, connections, number of drones, start hub, and end hub.
            visual (bool): Flag indicating whether to
            enable graphical visualization.
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
        """Checks if all drones have successfully reached the end hub.

        Returns:
            bool: True if every drone's status is 'finished', False otherwise.
        """
        return all(
            st["status"] == "finished" for st in self.drone_states.values()
        )

    def _format_move(self, drone_id: int, target: str) -> str:
        """Formats a move string for a specific drone and target
        node or connection, including current occupancy and capacity.

        Args:
            drone_id (int): The unique identifier of the drone.
            target (str): The target hub name or connection string.

        Returns:
            str: The formatted move command string (e.g., 'D1-hub2 [1/10]').
        """
        return f"D{drone_id}-{target}"

    def run_turn(self) -> List[str]:
        """Executes a single simulation turn, processing movements
        and transitions for all active drones based on their scheduled paths.

        Returns:
            List[str]: A list of move strings executed during this turn.
        """
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

                # Remove from current hub
                curr_hub_obj = self.hubs.get(curr_hub)
                if curr_hub_obj:
                    curr_hub_obj.drones_inside.discard(drone.id_num)

                next_hub_obj = self.hubs.get(next_hub)
                zone_type = (
                    next_hub_obj.zone_type if next_hub_obj else "normal"
                )

                if zone_type == "restricted" and next_hub != self.end_hub:
                    # Enters transit connection
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
        """Runs the complete simulation loop until all drones reach
        the destination or a deadlock is detected. Handles
        visualization updates and turn printing.
        """
        while not self.is_finished():
            moves = self.run_turn()
            if moves:
                self.output_turns.append(moves)
                print(" ".join(moves))

            if self.visualizer:
                self.visualizer.update(self.drones, self.current_turn)

            if not moves and not self.is_finished():
                if any(
                    st["status"] == "in_transit"
                    for st in self.drone_states.values()
                ):
                    continue
                print("❌ Simulation error: Deadlock detected.")
                break

    def save_output_txt(self, filepath: str = "output.txt") -> None:
        """Saves the complete sequence of simulation moves turn by turn to
        a text file.

        Args:
            filepath (str): The destination file path for the output log.
            Defaults to 'output.txt'.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                for turn_moves in self.output_turns:
                    f.write(" ".join(turn_moves) + "\n")
            print(f"\n💾 Output successfully saved to: {filepath}")
        except Exception as e:
            print(f"❌ Error saving output file: {e}")
