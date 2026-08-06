"""Módulo de representação do grafo e adjacências."""

from typing import Dict, List, Optional
from structure import Connection, Hub


class NetworkGraph:
    """Grafo da rede de zonas e conexões da simulação."""

    def __init__(self) -> None:
        self.hubs: Dict[str, Hub] = {}
        self.connections: Dict[str, Connection] = {}
        self.adj: Dict[str, List[str]] = {}
        self.start_hub: str = ""
        self.end_hub: str = ""

    def add_hub(self, hub: Hub) -> None:
        """Adiciona um nó ao grafo."""
        self.hubs[hub.name] = hub
        if hub.name not in self.adj:
            self.adj[hub.name] = []
        
        if hub.hub_type == "start":
            self.start_hub = hub.name
        elif hub.hub_type == "end":
            self.end_hub = hub.name

    def add_connection(self, conn: Connection) -> None:
        """Adiciona uma ligação bidirecional ao grafo."""
        link_key = "-".join(sorted([conn.from_hub, conn.to_hub]))
        self.connections[link_key] = conn
        self.adj.setdefault(conn.from_hub, []).append(conn.to_hub)
        self.adj.setdefault(conn.to_hub, []).append(conn.from_hub)

    def get_connection(self, u: str, v: str) -> Optional[Connection]:
        """Obtém o objeto de conexão entre dois nós."""
        link_key = "-".join(sorted([u, v]))
        return self.connections.get(link_key)