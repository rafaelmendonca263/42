import tkinter as tk
import time


class DroneVisualizer:
<<<<<<< HEAD
    def __init__(self, graph):
        if isinstance(graph, dict):
            self.hubs = graph.get("hubs", [])
            self.connections = graph.get("Connection", [])
        else:
            self.hubs = list(graph.hubs.values()) if hasattr(graph.hubs, 'values') else graph.hubs
            self.connections = list(graph.connections.values()) if hasattr(graph.connections, 'values') else graph.connections

        self.root = tk.Tk()
        self.root.title("42 Fly-in: Drone Fleet Simulator 🛸")
        
        # Alargamos a largura de 1100 para 1380 para caber o painel de texto à direita
        self.width = 1380
=======
    def __init__(self, graph_data):
        self.hubs = graph_data["hubs"]
        self.connections = graph_data["Connection"]

        self.root = tk.Tk()
        self.root.title("42 Fly-in: Drone Fleet Simulator 🛸")

        self.width = 1100
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9
        self.height = 750
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="#11111b"
        )
        self.canvas.pack()

        self.hub_coords = {}
        self._scale_coordinates()
        
        # Controlo de Input: Variável de bloqueio
        self.waiting_for_next_turn = True
        self.root.bind("<space>", self._on_space_pressed)

    def _on_space_pressed(self, event):
        """Liberta o bloqueio quando carregas no Espaço."""
        self.waiting_for_next_turn = False

    def _scale_coordinates(self):
        if not self.hubs:
            return
        min_x = min(h.x for h in self.hubs)
        max_x = max(h.x for h in self.hubs)
        min_y = min(h.y for h in self.hubs)
        max_y = max(h.y for h in self.hubs)

        padding = 80
        # O mapa gráfico agora usa apenas até aos 1100px de largura
        graph_width = 1100
        span_x = (max_x - min_x) if (max_x - min_x) != 0 else 1
        span_y = (max_y - min_y) if (max_y - min_y) != 0 else 1

        for hub in self.hubs:
<<<<<<< HEAD
            screen_x = padding + ((hub.x - min_x) / span_x) * (graph_width - 2 * padding)
            screen_y = padding + ((hub.y - min_y) / span_y) * (self.height - 2 * padding)
=======
            screen_x = padding + ((hub.x - min_x) / span_x) * (
                self.width - 2 * padding
            )
            screen_y = padding + ((hub.y - min_y) / span_y) * (
                self.height - 2 * padding
            )
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9
            self.hub_coords[hub.name] = (int(screen_x), int(screen_y))

    def draw_state(self, current_turn, drones_list, turn_output):
        self.canvas.delete("all")
<<<<<<< HEAD
        
        # Título da Simulação
        self.canvas.create_text(1100 // 2, 35, text=f"TURNO DE SIMULAÇÃO: {current_turn}", 
                                fill="#cdd6f4", font=("Helvetica", 22, "bold"))
=======

        self.canvas.create_text(
            self.width // 2,
            35,
            text=f"TURNO DE SIMULAÇÃO: {current_turn}",
            fill="#cdd6f4",
            font=("Helvetica", 22, "bold"),
        )
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9

        # 1. DESENHAR O GRAFO (Até à barreira dos 1100px)
        for conn in self.connections:
<<<<<<< HEAD
            if hasattr(conn, 'from_hub') and hasattr(conn, 'to_hub'):
                f_hub, t_hub = conn.from_hub, conn.to_hub
            else:
                continue
            if f_hub in self.hub_coords and t_hub in self.hub_coords:
                x1, y1 = self.hub_coords[f_hub]
                x2, y2 = self.hub_coords[t_hub]
                self.canvas.create_line(x1, y1, x2, y2, fill="#45475a", width=3)
=======
            if (
                conn.from_hub in self.hub_coords
                and conn.to_hub in self.hub_coords
            ):
                x1, y1 = self.hub_coords[conn.from_hub]
                x2, y2 = self.hub_coords[conn.to_hub]
                self.canvas.create_line(
                    x1, y1, x2, y2, fill="#45475a", width=3
                )
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9

        for hub in self.hubs:
            x, y = self.hub_coords[hub.name]
            r = 25
<<<<<<< HEAD
            if hub.hub_type == "start": color = "#a6e3a1"
            elif hub.hub_type == "end": color = "#f9e2af"
            elif getattr(hub, 'zone_type', '') == 'restricted': color = "#f38ba8"
            elif hasattr(hub, 'color') and hub.color: color = hub.color 
            else: color = "#89b4fa"
                
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="#cdd6f4", width=2)
            self.canvas.create_text(x, y, text=hub.name[:7], fill="#11111b", font=("Helvetica", 9, "bold"))
            if getattr(hub, 'max_drones', 1) > 1:
                self.canvas.create_text(x, y+38, text=f"max:{hub.max_drones}", fill="#bac2de", font=("Helvetica", 8))
=======

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
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9

        # 2. DESENHAR OS DRONES
        hub_drone_counters = {}
        for drone in drones_list:
            if (
                drone["current_hub"] == "impossible_goal"
                and not drone["is_flying"]
            ):
                continue
<<<<<<< HEAD
            current_hub = drone["current_hub"]
            if current_hub in self.hub_coords:
                x, y = self.hub_coords[current_hub]
                count = hub_drone_counters.get(current_hub, 0)
                hub_drone_counters[current_hub] = count + 1
                offset_x = (count % 4) * 14 - 21
                offset_y = (count // 4) * 14 + 38
                dx, dy = x + offset_x, y + offset_y
                self.canvas.create_rectangle(dx-6, dy-6, dx+6, dy+6, fill="#fab387", outline="#ffffff", width=1)
                self.canvas.create_text(dx, dy-12, text=f"D{drone['id']}", fill="#74c7ec", font=("Helvetica", 8, "bold"))

        # 3. PAINEL DE LOGS LATERAL (Dos 1100px aos 1380px)
        self.canvas.create_rectangle(1100, 0, 1380, 750, fill="#1e1e2e", outline="#313244", width=2)
        self.canvas.create_text(1240, 35, text="MOVIMENTOS DO TURNO", fill="#f5c2e7", font=("Helvetica", 13, "bold"))
        
        # Escreve as ações do turno na barra lateral
        y_offset = 80
        if not turn_output:
            self.canvas.create_text(1130, y_offset, text="• Nenhuns drones moveram-se.", fill="#a6adc8", font=("Helvetica", 11, "italic"), anchor="w")
        else:
            for log in turn_output:
                self.canvas.create_text(1130, y_offset, text=f"• {log}", fill="#a6e3a1", font=("Helvetica", 12, "bold"), anchor="w")
                y_offset += 28
                if y_offset > 650: # Evita transbordar o ecrã se houverem demasiados drones
                    self.canvas.create_text(1130, y_offset, text="... e mais", fill="#a6adc8", font=("Helvetica", 10), anchor="w")
                    break

        # Instrução de controlo no fundo do painel
        #  VERSÃO CORRIGIDA:
        self.canvas.create_rectangle(1120, 680, 1360, 730, fill="#313244", outline="#45475a", width=1)
        self.canvas.create_text(1240, 705, text="Pressiona [ESPAÇO] p/ avançar", fill="#f9e2af", font=("Helvetica", 10, "bold"))

        self.root.update()

        # LOOP DE BLOQUEIO ATÉ PREMIR O ESPAÇO
        self.waiting_for_next_turn = True
        while self.waiting_for_next_turn:
            self.root.update()
            time.sleep(0.02) # Alivia a carga no processador central
=======

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
>>>>>>> 196ff047d16a6436817ad5703c22743e41c379d9
