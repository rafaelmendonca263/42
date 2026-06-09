import tkinter as tk


class DroneVisualizer:
    def __init__(self, graph_data):
        self.hubs = graph_data["hubs"]
        self.connections = graph_data["Connection"]

        self.root = tk.Tk()
        self.root.title("42 Fly-in: Drone Fleet Simulator 🛸")

        self.width = 1100
        self.height = 750
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="#11111b"
        )
        self.canvas.pack()

        self.hub_coords = {}
        self._scale_coordinates()

    def _scale_coordinates(self):
        if not self.hubs:
            return

        min_x = min(h.x for h in self.hubs)
        max_x = max(h.x for h in self.hubs)
        min_y = min(h.y for h in self.hubs)
        max_y = max(h.y for h in self.hubs)

        padding = 80
        span_x = (max_x - min_x) if (max_x - min_x) != 0 else 1
        span_y = (max_y - min_y) if (max_y - min_y) != 0 else 1

        for hub in self.hubs:
            screen_x = padding + ((hub.x - min_x) / span_x) * (
                self.width - 2 * padding
            )
            screen_y = padding + ((hub.y - min_y) / span_y) * (
                self.height - 2 * padding
            )
            self.hub_coords[hub.name] = (int(screen_x), int(screen_y))

    def draw_state(self, current_turn, drones_list):
        self.canvas.delete("all")

        self.canvas.create_text(
            self.width // 2,
            35,
            text=f"TURNO DE SIMULAÇÃO: {current_turn}",
            fill="#cdd6f4",
            font=("Helvetica", 22, "bold"),
        )

        for conn in self.connections:
            if (
                conn.from_hub in self.hub_coords
                and conn.to_hub in self.hub_coords
            ):
                x1, y1 = self.hub_coords[conn.from_hub]
                x2, y2 = self.hub_coords[conn.to_hub]
                self.canvas.create_line(
                    x1, y1, x2, y2, fill="#45475a", width=3
                )

        for hub in self.hubs:
            x, y = self.hub_coords[hub.name]
            r = 25

            if hub.hub_type == "start":
                color = "#a6e3a1"
            elif hub.hub_type == "end":
                color = "#f9e2af"
            elif getattr(hub, "zone_type", "") == "restricted":
                color = "#f38ba8"
            elif hasattr(hub, "color") and hub.color:
                color = hub.color
            else:
                color = "#89b4fa"

            self.canvas.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill=color,
                outline="#cdd6f4",
                width=2,
            )
            self.canvas.create_text(
                x,
                y,
                text=hub.name[:7],
                fill="#11111b",
                font=("Helvetica", 9, "bold"),
            )

            if getattr(hub, "max_drones", 1) > 1:
                self.canvas.create_text(
                    x,
                    y + 38,
                    text=f"max:{hub.max_drones}",
                    fill="#bac2de",
                    font=("Helvetica", 8),
                )

        hub_drone_counters = {}
        for drone in drones_list:
            if (
                drone["current_hub"] == "impossible_goal"
                and not drone["is_flying"]
            ):
                continue

            current_hub = drone["current_hub"]
            if current_hub in self.hub_coords:
                x, y = self.hub_coords[current_hub]

                count = hub_drone_counters.get(current_hub, 0)
                hub_drone_counters[current_hub] = count + 1

                offset_x = (count % 4) * 14 - 21
                offset_y = (count // 4) * 14 + 38
                dx, dy = x + offset_x, y + offset_y

                self.canvas.create_rectangle(
                    dx - 6,
                    dy - 6,
                    dx + 6,
                    dy + 6,
                    fill="#fab387",
                    outline="#ffffff",
                    width=1,
                )
                self.canvas.create_text(
                    dx,
                    dy - 12,
                    text=f"D{drone['id']}",
                    fill="#74c7ec",
                    font=("Helvetica", 8, "bold"),
                )

        self.root.update()
