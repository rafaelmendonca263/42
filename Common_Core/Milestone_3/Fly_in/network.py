
from typing import Dict, List, Optional
from structure import Connection, Hub


class NetworkGraph:
    """Graph of the zone and connection network of the simulation."""
    def __init__(self) -> None:
        self.hubs: Dict[str, Hub] = {}
        self.connections: Dict[str, Connection] = {}
        self.adj: Dict[str, List[str]] = {}
        self.start_hub: str = ""
        self.end_hub: str = ""

    def add_hub(self, hub: Hub) -> None:
        """Adds a node to the graph."""
        self.hubs[hub.name] = hub
        if hub.name not in self.adj:
            self.adj[hub.name] = []

        if hub.hub_type == "start":
            self.start_hub = hub.name
        elif hub.hub_type == "end":
            self.end_hub = hub.name

    def add_connection(self, conn: Connection) -> None:
        "Adds a bidirectional link to the graph."
        link_key = "-".join(sorted([conn.from_hub, conn.to_hub]))
        self.connections[link_key] = conn
        self.adj.setdefault(conn.from_hub, []).append(conn.to_hub)
        self.adj.setdefault(conn.to_hub, []).append(conn.from_hub)

    def get_connection(self, u: str, v: str) -> Optional[Connection]:
        """Retrieves the connection object between two nodes."""
        link_key = "-".join(sorted([u, v]))
        return self.connections.get(link_key)
