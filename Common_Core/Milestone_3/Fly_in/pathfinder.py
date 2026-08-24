import heapq
from typing import List, Tuple, Dict, Optional
from structure import Hub, Connection
from reservation import ReservationTable


class SpaceTimeAStar:
    """Space-time route planner that prevents collisions and delays."""

    def __init__(
        self,
        hubs_map: Dict[str, Hub],
        connections_map: Dict[str, Connection],
        adj: Dict[str, List[str]],
        reservation_table: ReservationTable,
    ) -> None:
        self.hubs = hubs_map
        self.connections = connections_map
        self.adj = adj
        self.res = reservation_table

    @staticmethod
    def get_link_key(u: str, v: str) -> str:
        return "-".join(sorted([u, v]))

    def find_schedule(
        self, start_hub: str, end_hub: str, start_turn: int = 1
    ) -> List[Tuple[str, int]]:

        start_obj = self.hubs.get(start_hub)
        initial_priority_count = (1 if start_obj and
                                  start_obj.zone_type == "priority" else 0)

        pq: List[Tuple[int, int, int, str, List[Tuple[str, int]]]] = [
            (0, -initial_priority_count, start_turn, start_hub, [(start_hub,
                                                                  start_turn)])
        ]

        visited: Dict[Tuple[str, int], int] = {}

        while pq:
            _, neg_prio, t, curr, path = heapq.heappop(pq)
            prio_count = -neg_prio

            if curr == end_hub:
                return path

            state = (curr, t)
            if state in visited and visited[state] >= prio_count:
                continue
            visited[state] = prio_count

            curr_hub_obj = self.hubs.get(curr)
            max_c = curr_hub_obj.max_drones if curr_hub_obj else 1

            if curr == start_hub or self.res.is_hub_free(curr, t + 1, max_c):
                heapq.heappush(
                    pq, (t + 1, -prio_count, t + 1, curr, path +
                         [(curr, t + 1)])
                )

            for neighbor in self.adj.get(curr, []):
                neigh_obj = self.hubs.get(neighbor)
                if not neigh_obj:
                    continue

                if (
                    neigh_obj.zone_type == "blocked"
                    or neigh_obj.color == "black"
                ):
                    continue

                link_key = self.get_link_key(curr, neighbor)
                conn_obj: Optional[Connection] = self.connections.get(link_key)

                max_l_cap = conn_obj.max_drones if conn_obj else 1
                max_h_cap = neigh_obj.max_drones

                travel_duration = (
                    2 if neigh_obj.zone_type == "restricted" else 1
                )
                arrival_turn = t + travel_duration

                if not self.res.is_link_free(link_key, t, max_l_cap):
                    continue

                if neighbor != end_hub and not self.res.is_hub_free(
                    neighbor, arrival_turn, max_h_cap
                ):
                    continue

                new_prio_count = prio_count + (1 if neigh_obj.zone_type ==
                                               "priority" else 0)
                f_score = arrival_turn

                heapq.heappush(
                    pq,
                    (
                        f_score,
                        -new_prio_count,
                        arrival_turn,
                        neighbor,
                        path + [(neighbor, arrival_turn)],
                    ),
                )

        return []

    def commit_schedule(
        self, schedule: List[Tuple[str, int]], end_hub: str
    ) -> None:
        for i in range(len(schedule) - 1):
            curr_hub, curr_turn = schedule[i]
            next_hub, next_turn = schedule[i + 1]

            if curr_hub == next_hub:
                if curr_hub != schedule[0][0]:
                    self.res.reserve_hub(curr_hub, next_turn)
                continue

            link_key = self.get_link_key(curr_hub, next_hub)
            self.res.reserve_link(link_key, curr_turn)

            if next_hub != end_hub:
                self.res.reserve_hub(next_hub, next_turn)
