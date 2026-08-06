"""Motor de simulação otimizado pelo agendamento em Espaço-Tempo."""

from typing import List, Dict, Any, Union
from structure import Hub, Connection, Drone
from reservation import ReservationTable
from pathfinder import SpaceTimeAStar


class Simulation:
    def __init__(
        self,
        parsed_data: Dict[str, Any],
        visual: bool = False,
    ) -> None:
        self.hubs_list: List[Hub] = parsed_data["hubs"]
        self.raw_connections: List[Union[Connection, str]] = parsed_data["connections"]
        self.nb_drones: int = parsed_data["nb_drones"]
        self.start_hub: str = parsed_data["start_hub"]
        self.end_hub: str = parsed_data["end_hub"]
        self.visual = visual

        # Mapeamento O(1) de Hubs
        self.hubs: Dict[str, Hub] = {h.name: h for h in self.hubs_list}
        self.connections: Dict[str, Connection] = {}
        self.adj: Dict[str, List[str]] = {}

        # Mapeamento seguro de Conexões (trata instâncias de Connection ou Strings)
        for conn_item in self.raw_connections:
            if isinstance(conn_item, Connection):
                u, v = conn_item.from_hub, conn_item.to_hub
                conn_obj = conn_item
            elif isinstance(conn_item, str):
                parts = conn_item.split("-") if "-" in conn_item else conn_item.split()
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

        # Inicialização dos Drones
        self.drones: List[Drone] = []
        self.drone_states: Dict[int, Dict[str, Any]] = {}

        for i in range(1, self.nb_drones + 1):
            schedule = self.pathfinder.find_schedule(self.start_hub, self.end_hub)
            if schedule:
                self.pathfinder.commit_schedule(schedule, self.end_hub)

            path_nodes = [node for node, _ in schedule]
            drone_obj = Drone(id_num=i, current_hub=self.start_hub, path=path_nodes)
            self.drones.append(drone_obj)

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
        return all(st["status"] == "finished" for st in self.drone_states.values())

    def run_turn(self) -> List[str]:
        self.current_turn += 1
        turn_moves: List[str] = []

        for drone in self.drones:
            st = self.drone_states[drone.id_num]

            if st["status"] == "finished":
                continue

            # 1. Trânsito para Zonas Restritas (2º turno da transição)
            if st["status"] == "in_transit":
                target_hub = st["in_transit_to"]
                st["in_transit_to"] = None
                drone.current_hub = target_hub

                if target_hub == self.end_hub:
                    st["status"] = "finished"
                else:
                    st["status"] = "moving"

                # Formato Subject VII.5: D<ID>-<zone>
                turn_moves.append(f"D{drone.id_num}-{target_hub}")
                continue

            # 2. Execução do movimento agendado
            schedule = st["schedule"]
            idx = st["schedule_idx"]

            if idx >= len(schedule) - 1:
                continue

            curr_hub, curr_t = schedule[idx]
            next_hub, next_t = schedule[idx + 1]

            if self.current_turn == curr_t:
                st["schedule_idx"] += 1

                # Se for espera agendada no mesmo nó, não emite instrução de movimento
                if curr_hub == next_hub:
                    continue

                next_hub_obj = self.hubs.get(next_hub)
                zone_type = next_hub_obj.zone_type if next_hub_obj else "normal"

                if zone_type == "restricted" and next_hub != self.end_hub:
                    st["status"] = "in_transit"
                    st["in_transit_to"] = next_hub
                    # Formato Subject VII.5: D<ID>-<connection>
                    conn_name = f"{curr_hub}-{next_hub}"
                    turn_moves.append(f"D{drone.id_num}-{conn_name}")
                else:
                    drone.current_hub = next_hub
                    if next_hub == self.end_hub:
                        st["status"] = "finished"
                    else:
                        st["status"] = "moving"
                    # Formato Subject VII.5: D<ID>-<zone>
                    turn_moves.append(f"D{drone.id_num}-{next_hub}")

        return turn_moves

    def run(self) -> None:
        while not self.is_finished():
            moves = self.run_turn()
            if moves:
                self.output_turns.append(moves)
                print(" ".join(moves))

            if self.visualizer:
                self.visualizer.update(self.drones, self.current_turn)

            if not moves and not self.is_finished():
                if any(st["status"] == "in_transit" for st in self.drone_states.values()):
                    continue
                print("❌ Erro: Simulação em impasse.")
                break

    def save_output_txt(self, filepath: str = "output.txt") -> None:
        """Opcional: Guarda a saída do terminal num ficheiro de texto (.txt)."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                for turn_moves in self.output_turns:
                    f.write(" ".join(turn_moves) + "\n")
            print(f"\n💾 Output gravado com sucesso em: {filepath}")
        except Exception as e:
            print(f"❌ Erro ao gravar ficheiro de output: {e}")