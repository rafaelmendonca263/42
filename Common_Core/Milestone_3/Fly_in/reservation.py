"""Módulo para gestão da tabela de reservas em espaço-tempo."""

from typing import Dict, Tuple


class ReservationTable:
    """Tabela de reservas temporal para nós e conexões no grafo."""

    def __init__(self) -> None:
        # (hub_name, turn) -> count
        self.hub_reservations: Dict[Tuple[str, int], int] = {}
        # (link_key, turn) -> count
        self.link_reservations: Dict[Tuple[str, int], int] = {}

    def is_hub_free(self, hub_name: str, turn: int, max_cap: int) -> bool:
        return self.hub_reservations.get((hub_name, turn), 0) < max_cap

    def is_link_free(self, link_key: str, turn: int, max_cap: int) -> bool:
        return self.link_reservations.get((link_key, turn), 0) < max_cap

    def reserve_hub(self, hub_name: str, turn: int) -> None:
        key = (hub_name, turn)
        self.hub_reservations[key] = self.hub_reservations.get(key, 0) + 1

    def reserve_link(self, link_key: str, turn: int) -> None:
        key = (link_key, turn)
        self.link_reservations[key] = self.link_reservations.get(key, 0) + 1