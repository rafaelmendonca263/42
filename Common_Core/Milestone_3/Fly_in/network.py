from typing import Any, Dict, List, Tuple
from structure import Hub, Connection


class NetworkGraph:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.hubs: Dict[str, Hub] = {}
        self.connections: Dict[str, Connection] = {}
        self.adj_list: Dict[str, List[str]] = {}
        self._paths_cache: Dict[str, List[Tuple[List[str], int]]] = {}

        if data:
            for hub in data.get("hubs", []):
                self.add_hub(hub)
            for conn in data.get("Connection", []):
                self.add_connection(conn)

    def add_hub(self, hub: Hub) -> None:
        self.hubs[hub.name] = hub
        self.adj_list[hub.name] = []

    def add_connection(self, conn: Connection) -> None:
        key = f"{conn.from_hub}->{conn.to_hub}"
        self.connections[key] = conn
        if conn.to_hub not in self.adj_list[conn.from_hub]:
            self.adj_list[conn.from_hub].append(conn.to_hub)
        self._paths_cache.clear()

    def find_all_paths(self, start: str, end: str) -> List[Tuple[List[str], int]]:
        cache_key = f"{start}->{end}"
        if cache_key in self._paths_cache:
            return self._paths_cache[cache_key]

        calculated_paths = self._dfs_find_paths(start, end, [])

        # Guarda na cache para otimização de performance
        self._paths_cache[cache_key] = calculated_paths
        return calculated_paths

    def _dfs_find_paths(
        self, start: str, end: str, current_path: List[str]
    ) -> List[Tuple[List[str], int]]:
        """Mecanismo DFS interno protegido para mapear rotas."""
        path = current_path + [start]

        if start == end:
            return [(path, len(path) - 1)]

        if start not in self.adj_list:
            return []

        paths: List[Tuple[List[str], int]] = []
        for node in self.adj_list[start]:
            if node not in path:
                newpaths = self._dfs_find_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
