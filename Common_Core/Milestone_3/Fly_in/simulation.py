from structure import Drone
from network import NetworkGraph

class Simulation:
    def __init__(self, graph: NetworkGraph, nb_drones: int, start_hub: str, end_hub: str):
        self.graph = graph

        self.drones = [
            {
                "id": i, 
                "current_hub": start_hub, 
                "path": None, 
                "step": 0,
                "start_turn": 0
            } 
            for i in range(1, nb_drones + 1)
        ]
        self.end_hub = end_hub
        self.current_turn = 0

        self.available_paths = self.graph.find_all_paths(start_hub, end_hub)
        self.available_paths.sort(key=lambda x: x[1])

        self.hub_occupancy = {}
        self.conn_occupancy = {}

    def run(self):
        while not self.all_drones_arrived():
            print(f"\n--- Turno Atual: {self.current_turn} ---")

            for drone in self.drones:
                if drone["current_hub"] == self.end_hub:
                    continue

                if drone["path"] is None:
                    best_path = self.evaluate_best_path(self.current_turn)
                    drone["path"] = best_path
                    drone["step"] = 0

                self.move_drone(drone)
            
            self.current_turn += 1
            
        print(f"\nSimulação concluída em {self.current_turn} turnos!")

    def all_drones_arrived(self) -> bool:
        return all(drone["current_hub"] == self.end_hub for drone in self.drones)

    def evaluate_best_path(self, start_turn: int):
        best_path = None
        best_arrival_turn = float('inf') # Começamos com um valor infinito

        for path, theoretical_cost in self.available_paths:
            arrival_turn = self.simulate_path_arrival(path, start_turn)

            if arrival_turn < best_arrival_turn:
                best_arrival_turn = arrival_turn
                best_path = path
                
        return best_path
    
    def simulate_path_arrival(self, path: list, start_turn: int) -> int:
        current_time = start_turn

        for i in range(1, len(path)):
            next_hub_name = path[i]
            
            # Acedemos ao objeto Hub real para ver as suas propriedades
            hub_object = self.graph.hubs[next_hub_name]
            
            # Determinamos o custo de tempo com base no zone_type
            if hub_object.zone_type == "restricted":
                travel_cost = 2
            else:
                travel_cost = 1  # normal, priority, etc.
                
            # O drone tenta chegar ao próximo hub neste turno futuro
            arrival_time = current_time + travel_cost
            
            # ... Aqui precisamos de validar as agendas de ocupação ...
            
            # Se estiver tudo livre, o tempo atual passa a ser o tempo de chegada
            current_time = arrival_time
            
        return current_time