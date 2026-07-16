import time
from network import NetworkGraph
from visualizer import DroneVisualizer


class Simulation:
    def __init__(
        self,
        graph: NetworkGraph,
        nb_drones: int,
        start_hub: str,
        end_hub: str,
        visual: bool = False,
    ):
        self.graph = graph
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.current_turn = 0
        self.output_history: list = []
        self.visual = visual

        # Estado inicial dos drones (com suporte a verificação de status unificada)
        self.drones = [
            {
                "id": i,
                "current_hub": start_hub,
                "path": None,
                "step": 0,
                "start_turn": 0,
                "lock_until_turn": 0,
                "is_flying": False,
                "status": "landed",
            }
            for i in range(1, nb_drones + 1)
        ]

        # Tabelas de ocupação dinâmicas {turno: {nome_hub: contagem}}
        self.hub_occupancy: dict = {}
        self.conn_occupancy: dict = {}

        # Inicializa o visualizador apenas se a flag visual estiver ativa
        if self.visual:
            self.visualizer = DroneVisualizer(self.graph)

    def run(self) -> None:
        """Loop principal formatado rigorosamente de acordo com a norma da 42."""
        max_turn_limit = 1000  # Fail-safe

        while not self.all_drones_arrived() and self.current_turn < max_turn_limit:
            # Lista para guardar os outputs deste turno específico (ex: "D1-gate_hell1")
            turn_output = []

            # FASE 1: Registar ocupação estática dos drones que começam o turno em terra
            for drone in self.drones:
                if drone["current_hub"] == self.end_hub:
                    continue
                if (
                    self.current_turn >= drone["lock_until_turn"]
                    and not drone["is_flying"]
                ):
                    self.register_hub_occupancy(self.current_turn, drone["current_hub"])

            # FASE 2: Processar cada drone (Ordenados por ID de 1 a N)
            for drone in self.drones:
                if drone["current_hub"] == self.end_hub:
                    continue

                # 1. Processar Aterragens
                if self.current_turn == drone["lock_until_turn"] and drone["is_flying"]:
                    self.unregister_hub_occupancy(
                        self.current_turn, drone["current_hub"]
                    )

                    drone["step"] += 1
                    drone["current_hub"] = drone["path"][drone["step"]]
                    drone["is_flying"] = False
                    drone["status"] = "landed"

                    # Se aterrou no destino final, não regista mais ocupação
                    if drone["current_hub"] != self.end_hub:
                        self.register_hub_occupancy(
                            self.current_turn, drone["current_hub"]
                        )

                # 2. Se o drone ainda está no meio de um voo longo (Restricted Zone)
                if self.current_turn < drone["lock_until_turn"] and drone["is_flying"]:
                    # Regra do enunciado: em pleno voo para zona restrita, mostra a conexão
                    current_step = drone["step"]
                    origem = drone["path"][current_step]
                    destino = drone["path"][current_step + 1]
                    turn_output.append(f"D{drone['id']}-{origem}-{destino}")
                    continue

                # 3. Tomada de Decisão e Descolagem para drones livres no chão
                if (
                    self.current_turn >= drone["lock_until_turn"]
                    and not drone["is_flying"]
                ):
                    best_path = self.evaluate_best_path(
                        drone["current_hub"], self.current_turn
                    )

                    if best_path and len(best_path) > 1:
                        drone["path"] = best_path
                        drone["step"] = 0

                        current_hub_name = drone["current_hub"]
                        next_hub_name = best_path[1]

                        hub_object = self.graph.hubs[next_hub_name]
                        conn_object = self.graph.connections.get(
                            f"{current_hub_name}->{next_hub_name}"
                        )

                        travel_cost = 2 if hub_object.zone_type == "restricted" else 1
                        arrival_time = self.current_turn + travel_cost

                        # Validar capacidades de Hub
                        hubs_agendados = self.hub_occupancy.get(arrival_time, {}).get(
                            next_hub_name, 0
                        )
                        hub_ok = hubs_agendados < hub_object.max_drones

                        # Validar capacidades de Conexão
                        conn_key = f"{current_hub_name}->{next_hub_name}"
                        conn_ok = True
                        if conn_object:
                            for t in range(self.current_turn, arrival_time):
                                drones_na_conn = self.conn_occupancy.get(t, {}).get(
                                    conn_key, 0
                                )
                                if drones_na_conn >= conn_object.max_drones:
                                    conn_ok = False
                                    break

                        if hub_ok and conn_ok:
                            # Efetivar movimento e ocupar os recursos para as janelas futuras
                            self.register_hub_occupancy(arrival_time, next_hub_name)
                            if conn_object:
                                for t in range(self.current_turn, arrival_time):
                                    self.register_conn_occupancy(t, conn_key)

                            drone["lock_until_turn"] = arrival_time
                            drone["is_flying"] = True
                            drone["status"] = "in_transit"

                            # Saída formatada baseada no tempo de voo
                            if travel_cost == 2:
                                turn_output.append(
                                    f"D{drone['id']}-{current_hub_name}-{next_hub_name}"
                                )
                            else:
                                turn_output.append(f"D{drone['id']}-{next_hub_name}")
                        else:
                            drone["lock_until_turn"] = self.current_turn + 1
                            drone["path"] = None
                    else:
                        drone["lock_until_turn"] = self.current_turn + 1

            if turn_output:
                turn_output.sort(key=lambda x: int(x.split("-")[0][1:]))
                print(" ".join(turn_output))
                self.output_history.append(" ".join(turn_output))

            if self.visual:
                self.visualizer.draw_state(self.current_turn, self.drones, turn_output)

            self.current_turn += 1

    def register_hub_occupancy(self, turn: int, hub_name: str) -> None:
        if turn not in self.hub_occupancy:
            self.hub_occupancy[turn] = {}
        if hub_name not in self.hub_occupancy[turn]:
            self.hub_occupancy[turn][hub_name] = 0
        self.hub_occupancy[turn][hub_name] += 1

    def unregister_hub_occupancy(self, turn: int, hub_name: str) -> None:
        if turn in self.hub_occupancy and hub_name in self.hub_occupancy[turn]:
            self.hub_occupancy[turn][hub_name] -= 1
            if self.hub_occupancy[turn][hub_name] <= 0:
                del self.hub_occupancy[turn][hub_name]

    def register_conn_occupancy(self, turn: int, conn_key: str) -> None:
        if turn not in self.conn_occupancy:
            self.conn_occupancy[turn] = {}
        if conn_key not in self.conn_occupancy[turn]:
            self.conn_occupancy[turn][conn_key] = 0
        self.conn_occupancy[turn][conn_key] += 1

    def unregister_conn_occupancy(self, turn: int, conn_key: str) -> None:
        if turn in self.conn_occupancy and conn_key in self.conn_occupancy[turn]:
            self.conn_occupancy[turn][conn_key] -= 1
            if self.conn_occupancy[turn][conn_key] <= 0:
                del self.conn_occupancy[turn][conn_key]

    def all_drones_arrived(self) -> bool:
        return all(drone["current_hub"] == self.end_hub for drone in self.drones)

    def evaluate_best_path(self, current_hub: str, start_turn: int) -> list:
        """Avalia e escolhe o melhor caminho livre com simulação de tráfego futuro."""
        all_paths = self.graph.find_all_paths(current_hub, self.end_hub)
        if not all_paths:
            return []

        best_path = None
        best_arrival = float("inf")

        for path_data in all_paths:
            # O find_all_paths devolve uma lista de tuplos: (lista_do_caminho, custo)
            path = path_data[0]

            # Simula a viagem por este caminho a partir do tempo atual
            sim_time = start_turn
            possible = True

            for index in range(len(path) - 1):
                u = path[index]
                v = path[index + 1]

                hub_object = self.graph.hubs[v]
                conn_object = self.graph.connections.get(f"{u}->{v}")

                cost = 2 if hub_object.zone_type == "restricted" else 1
                arrival = sim_time + cost

                # Verifica conflito no hub de destino no instante da aterragem
                drones_no_hub = self.hub_occupancy.get(arrival, {}).get(v, 0)
                if drones_no_hub >= hub_object.max_drones:
                    possible = False
                    break

                # Verifica conflito na conexão durante os turnos de travessia
                if conn_object:
                    conn_key = f"{u}->{v}"
                    for t in range(sim_time, arrival):
                        drones_na_conn = self.conn_occupancy.get(t, {}).get(conn_key, 0)
                        if drones_na_conn >= conn_object.max_drones:
                            possible = False
                            break
                    if not possible:
                        break

                sim_time = arrival

            # Se o caminho for realizável sem colisões e chegar mais rápido que os outros
            if possible and sim_time < best_arrival:
                best_arrival = sim_time
                best_path = path

        # Se nenhum caminho direto está livre, o drone aguarda (retorna lista vazia)
        return best_path if best_path else []

    def save_output(self, filename: str = "output.json") -> None:
        import json

        data_to_save = {
            "total_turns": self.current_turn,
            "hubs_end_state": {d["id"]: d["current_hub"] for d in self.drones},
            "steps": self.output_history
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        print(f"\n💾 Output da simulação gravado com sucesso em: {filename}")
