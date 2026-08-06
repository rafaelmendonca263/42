import sys
import pygame
from typing import Dict, Any, List, Tuple

COLOR_MAP: Dict[str, Tuple[int, int, int]] = {
    "green": (46, 204, 113),  # Start
    "red": (231, 76, 60),  # End / Danger
    "blue": (52, 152, 219),  # Normal
    "purple": (155, 89, 182),  # Maze traps
    "orange": (230, 126, 34),  # Micro gates
    "maroon": (128, 0, 0),  # Overflow
    "brown": (139, 69, 19),  # Restricted loops
    "gold": (241, 196, 15),  # Priority / False hope
    "darkred": (139, 0, 0),  # Convergence
    "violet": (142, 68, 173),  # Merge
    "crimson": (220, 20, 60),  # Torture gauntlet
    "black": (40, 40, 40),  # Dead ends / Blocked
    "cyan": (26, 188, 156),  # Final stretch
}


class DroneVisualizer:
    def __init__(
        self,
        simulation: Any,
        width: int = 1600,
        height: int = 950,
        bg_image_path: str = "Background.jpg",
    ):
        pygame.init()
        pygame.display.set_caption("Fly_in - Simulation Visualizer")

        self.sim = simulation
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        # 🔤 Fontes ultra-compactas (tamanho 8) para máxima clareza
        self.font = pygame.font.SysFont("Arial", 8, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 15, bold=True)

        self.bg_image = None
        try:
            image = pygame.image.load(bg_image_path)
            self.bg_image = pygame.transform.scale(
                image, (width, height)
            ).convert()
        except Exception as e:
            print(
                f"⚠️ Não foi possível carregar a imagem '{bg_image_path}': {e}"
            )
            print("A utilizar fundo escuro de reserva.")

        self.node_positions = self._calculate_node_positions()

    def _calculate_node_positions(self) -> Dict[str, Tuple[int, int]]:
        hubs = getattr(self.sim, "hubs", {})
        if not hubs:
            return {}

        xs = [h.x for h in hubs.values()]
        ys = [h.y for h in hubs.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        padding_x = 140
        padding_y = 130

        x_span = (max_x - min_x) if max_x != min_x else 1
        y_span = (max_y - min_y) if max_y != min_y else 1

        positions = {}
        for name, hub in hubs.items():
            px = padding_x + int(
                (hub.x - min_x) / x_span * (self.width - 2 * padding_x)
            )
            py = padding_y + int(
                (hub.y - min_y) / y_span * (self.height - 2 * padding_y)
            )
            positions[name] = (px, py)

        return positions

    def _get_hub_color(
        self, hub: Any, current_turn: int
    ) -> Tuple[int, int, int]:
        color_attr = getattr(hub, "color", None)

        if color_attr and str(color_attr).lower() == "rainbow":
            time_ms = pygame.time.get_ticks()
            hue = (time_ms // 8) % 360
            rainbow_color = pygame.Color(0)
            rainbow_color.hsva = (hue, 100, 100, 100)
            return (rainbow_color.r, rainbow_color.g, rainbow_color.b)

        if color_attr and str(color_attr).lower() in COLOR_MAP:
            return COLOR_MAP[str(color_attr).lower()]

        hub_type = getattr(hub, "hub_type", "normal")
        zone_type = getattr(hub, "zone_type", "normal")

        if hub_type == "start":
            return COLOR_MAP["green"]
        if hub_type == "end":
            return COLOR_MAP["red"]
        if zone_type == "restricted":
            return COLOR_MAP["orange"]
        if zone_type == "priority":
            return COLOR_MAP["gold"]
        if zone_type == "blocked":
            return COLOR_MAP["black"]

        return COLOR_MAP["blue"]

    def _draw_background(self) -> None:
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((15, 23, 42))

    def _draw_text_with_outline(
        self,
        text: str,
        font: pygame.font.Font,
        text_color: Tuple[int, int, int],
        outline_color: Tuple[int, int, int],
        pos: Tuple[int, int],
    ) -> None:
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)

        for dx, dy in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (1, 1),
            (-1, 1),
            (1, -1),
        ]:
            self.screen.blit(outline_surface, (pos[0] + dx, pos[1] + dy))

        self.screen.blit(text_surface, pos)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit(0)

    def update(self, drones: Any, current_turn: int) -> None:
        self.handle_events()
        self._draw_background()

        # 1. Conexões / Arestas
        connections = getattr(self.sim, "connections", {})
        conn_iterable = (
            connections.values()
            if isinstance(connections, dict)
            else connections
        )

        for conn in conn_iterable:
            if hasattr(conn, "from_hub") and hasattr(conn, "to_hub"):
                u_pos = self.node_positions.get(conn.from_hub)
                v_pos = self.node_positions.get(conn.to_hub)
                if u_pos and v_pos:
                    pygame.draw.line(
                        self.screen, (180, 190, 210), u_pos, v_pos, 2
                    )

        # 2. Hubs (Círculos + Nomes em fonte tamanho 8)
        hubs = getattr(self.sim, "hubs", {})
        for name, pos in self.node_positions.items():
            hub = hubs.get(name)
            if not hub:
                continue

            color = self._get_hub_color(hub, current_turn)

            pygame.draw.circle(self.screen, color, pos, 12)
            pygame.draw.circle(self.screen, (241, 245, 249), pos, 12, 2)

            label = self.font.render(name, True, (0, 0, 0))
            text_x = pos[0] - label.get_width() // 2
            text_y = pos[1] - 18
            self._draw_text_with_outline(
                name, self.font, (0, 0, 0), (255, 255, 255), (text_x, text_y)
            )

        # 3. Drones Ativos em Grelha (2 por linha com texto tamanho 8)
        MAX_PER_ROW = 2
        drones_by_hub: Dict[str, List[Any]] = {}
        for drone in drones:
            status = getattr(drone, "status", None) or (
                drone.get("status") if isinstance(drone, dict) else None
            )
            current_hub = getattr(drone, "current_hub", None) or (
                drone.get("current_hub") if isinstance(drone, dict) else None
            )

            if status != "finished" and current_hub:
                drones_by_hub.setdefault(current_hub, []).append(drone)

        for hub_name, hub_drones in drones_by_hub.items():
            base_pos = self.node_positions.get(hub_name)
            if not base_pos:
                continue

            spacing_x = 14
            spacing_y = 12
            y_offset = 15

            for idx, drone in enumerate(hub_drones):
                drone_id = getattr(drone, "id_num", None) or (
                    drone.get("id") if isinstance(drone, dict) else None
                )

                col = idx % MAX_PER_ROW
                row = idx // MAX_PER_ROW

                total_in_row = min(
                    MAX_PER_ROW, len(hub_drones) - row * MAX_PER_ROW
                )
                row_start_x = (
                    base_pos[0] - ((total_in_row - 1) * spacing_x) // 2
                )
                px = row_start_x + (col * spacing_x)
                py = base_pos[1] + y_offset + (row * spacing_y)

                # Ponto do Drone
                pygame.draw.circle(self.screen, (250, 204, 21), (px, py), 3)
                pygame.draw.circle(self.screen, (15, 23, 42), (px, py), 3, 1)

                # ID do Drone
                d_str = f"D{drone_id}"
                self._draw_text_with_outline(
                    d_str,
                    self.font,
                    (0, 0, 0),
                    (255, 255, 255),
                    (px - 4, py + 2),
                )

        # 4. HUD do Turno
        self._draw_text_with_outline(
            f"TURNO: {current_turn}",
            self.title_font,
            (0, 0, 0),
            (255, 255, 255),
            (20, 20),
        )

        pygame.display.flip()
        self.clock.tick(3)
