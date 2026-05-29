from collections import deque

class NetworkGraph:
    def __init__(self, parsed_data):
        self.hubs = {hub.name: hub for hub in parsed_data["hubs"]}

        self.adj = {hub_name: [] for hub_name in self.hubs}
        
        for conn in parsed_data["Connection"]:
            self.adj[conn.hub1].append(conn.hub2)
            self.adj[conn.hub2].append(conn.hub1)
    
    def find_all_paths(self, start: str, end: str):

        queue = deque([[start]])
        paths = []
        path = []
        current_cost = 0

        while queue:
            path, current_cost = queue.popleft()
            current_hub = path[-1]
            
            if current_hub == end:
                paths.append((path, current_cost))
                continue

            for neighbour in self.adj[current_hub]:
                if neighbour not in path: 
                    neighbour_hub = self.hubs[neighbour]
                    if self.hubs[neighbour].zone_type == "blocked":
                        continue
                    elif neighbour_hub.zone_type == "restricted":
                        additional_cost = 2
                    else:
                        additional_cost = 1
                    new_cost = current_cost + additional_cost
                    new_path = path + [neighbour]
                    queue.append((new_path, new_cost))
                
        return paths
