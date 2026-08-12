import sys
import pygame
from typing import Dict, Any, List, Tuple

COLOR_MAP: Dict[str, Tuple[int, int, int]] = {
    "green": (46, 204, 113),
    "red": (231, 76, 60),
    "blue": (52, 152, 219),
    "purple": (155, 89, 182),
    "orange": (230, 126, 34),
    "maroon": (128, 0, 0),
    "brown": (139, 69, 19),
    "gold": (241, 196, 15),
    "darkred": (139, 0, 0),
    "violet": (142, 68, 173),
    "crimson": (220, 20, 60),
    "black": (40, 40, 40),
    "cyan": (26, 188, 156),
}


class DroneVisualizer:
    def __init__(
        self,
        simulation: Any,
        width: int = 1600,
        height: int = 950,
        bg_image_path: str = "Background.jpg",
    ) -> None:
        """Initializes the Pygame viewer window and calculates
        the initial positions of the hubs.

        Args:

        simulation (Any): Instance of the running simulation.

        width (int): Width of the viewport window. Defaults to 1600.

        height (int): Height of the viewport window. Defaults to 950.

        bg_image_path (str): Path to the map background image.
        Defaults to "Background.jpg".
        """

        pygame.init()
        pygame.display.set_caption("Fly_in - Simulation Visualizer")

        self.sim = simulation
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

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
                f"The image could not be loaded: '{bg_image_path}': {e}"
            )
            print("Using a dark background as a backup.")

        self.node_positions = self._calculate_node_positions()

    def _calculate_node_positions(self) -> Dict[str, Tuple[int, int]]:
        """Maps and scales the Cartesian coordinates of the hubs to pixels
        on the screen.

        Returns:

        Dict[str, Tuple[int, int]]: Dictionary with the hub name and
        its coordinates (x, y) on the screen.

        """

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
        """Determines the rendering color of a hub based on
        its properties or zone type.

        Args:

        hub (Any): Hub object to evaluate.

        current_turn (int): Current turn of the simulation
        (used for animations like 'rainbow').

        Returns:

        Tuple[int, int, int]: RGB tuple with the corresponding color.

        """
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
        """Draws the background image or a filled backup
        background on the screen."""
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
        """Draws text on the screen with an outline to make it
        easier to read on dynamic backgrounds.

        Args:

        text (str): Text to be drawn.
        font (pygame.font.Font): Font object used.
        text_color (Tuple[int, int, int]): Main text color (RGB).
        outline_color (Tuple[int, int, int]): Outline color (RGB).
        pos (Tuple[int, int]): Coordinates (x, y) of position on the screen.

        """

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
        """Processes user input events (such as closing the window
        or pressing ESC)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit(0)

    def update(self, drones: Any, current_turn: int) -> None:
        """Updates and redraws the entire screen with the current state of
        the drones, hubs, and connections.

        Args:

        drones (Any): List of drone objects in the simulation.

        current_turn (int): Current turn number.

        """

        self.handle_events()
        self._draw_background()

        # 1. Connections / Edges
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

        # 2. Hubs
        hubs = getattr(self.sim, "hubs", {})
        for name, pos in self.node_positions.items():
            hub = hubs.get(name)
            if not hub:
                continue

            color = self._get_hub_color(hub, current_turn)

            pygame.draw.circle(self.screen, color, pos, 25)
            pygame.draw.circle(self.screen, (241, 245, 249), pos, 25, 2)

            text_x = pos[0] - self.font.size(name)[0] // 2
            text_y = pos[1] - 30
            self._draw_text_with_outline(
                name, self.font, (0, 0, 0), (255, 255, 255), (text_x, text_y)
            )

        # 3. Drones (Separated between Hubs and in Transit on Connections)
        MAX_PER_ROW = 2
        drones_by_hub: Dict[str, List[Any]] = {}
        drones_in_transit: List[Tuple[Any, Tuple[str, str]]] = []

        for drone in drones:
            status = getattr(drone, "status", None)
            if status == "finished":
                continue

            transit_conn = getattr(drone, "transit_connection", None)
            if transit_conn:
                drones_in_transit.append((drone, transit_conn))
            else:
                current_hub = getattr(drone, "current_hub", None)
                if current_hub:
                    drones_by_hub.setdefault(current_hub, []).append(drone)

        # Designing Drones in Hubs
        for hub_name, hub_drones in drones_by_hub.items():
            base_pos = self.node_positions.get(hub_name)
            if not base_pos:
                continue

            spacing_x = 14
            spacing_y = 12
            y_offset = 15

            for idx, drone in enumerate(hub_drones):
                drone_id = getattr(drone, "id_num", None)
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

                pygame.draw.circle(self.screen, (250, 204, 21), (px, py), 3)
                pygame.draw.circle(self.screen, (15, 23, 42), (px, py), 3, 1)

                d_str = f"D{drone_id}"
                self._draw_text_with_outline(
                    d_str,
                    self.font,
                    (0, 0, 0),
                    (255, 255, 255),
                    (px - 4, py + 2),
                )

        # Drawing Drones in Transit (Stopped at Connection)
        for drone, (u_hub, v_hub) in drones_in_transit:
            u_pos = self.node_positions.get(u_hub)
            v_pos = self.node_positions.get(v_hub)
            if u_pos and v_pos:
                mid_x = (u_pos[0] + v_pos[0]) // 2
                mid_y = (u_pos[1] + v_pos[1]) // 2

                pygame.draw.circle(self.screen, (250, 204, 21),
                                   (mid_x, mid_y), 4)
                pygame.draw.circle(self.screen, (230, 126, 34),
                                   (mid_x, mid_y), 4, 1)

                drone_id = getattr(drone, "id_num", None)
                d_str = f"D{drone_id}"
                self._draw_text_with_outline(
                    d_str,
                    self.font,
                    (0, 0, 0),
                    (255, 255, 255),
                    (mid_x - 4, mid_y + 4),
                )

        # 4. Turn HUD
        self._draw_text_with_outline(
            f"TURNO: {current_turn}",
            self.title_font,
            (0, 0, 0),
            (255, 255, 255),
            (20, 20),
        )

        pygame.display.flip()
        self.clock.tick(5)
