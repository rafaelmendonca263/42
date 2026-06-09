from structure import Hub, Connection


class NetworkGraph:
    def __init__(self):
        self.hubs = {}
        self.connections = {}
        self.adj_list = {}
        # Cache interna para não repetir o DFS de hubs já calculados
        self._paths_cache = {}

    def add_hub(self, hub: Hub):
        self.hubs[hub.name] = hub
        self.adj_list[hub.name] = []

    def add_connection(self, conn: Connection):
        key = f"{conn.from_hub}->{conn.to_hub}"
        self.connections[key] = conn
        # Garante que não adicionas duplicados se o parser ler a mesma linha
        if conn.to_hub not in self.adj_list[conn.from_hub]:
            self.adj_list[conn.from_hub].append(conn.to_hub)
        # Limpa a cache se novas conexões forem adicionadas dinamicamente
        self._paths_cache.clear()

    def find_all_paths(self, start: str, end: str):
        """Procura caminhos usando cache para evitar explosão combinatória no DFS."""
        cache_key = f"{start}->{end}"
        if cache_key in self._paths_cache:
            return self._paths_cache[cache_key]

        # Executa o DFS real apenas se não estiver na cache
        calculated_paths = self._dfs_find_paths(start, end, [])

        # Guarda na cache
        self._paths_cache[cache_key] = calculated_paths
        return calculated_paths

    def _dfs_find_paths(self, start: str, end: str, current_path: list) -> list:
        """Mecanismo DFS interno protegido."""
        path = current_path + [start]

        if start == end:
            return [(path, len(path) - 1)]

        if start not in self.adj_list:
            return []

        paths = []
        for node in self.adj_list[start]:
            if node not in path:
                newpaths = self._dfs_find_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
