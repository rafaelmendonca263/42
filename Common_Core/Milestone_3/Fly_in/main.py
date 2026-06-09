import sys
from parser import parse_config
from simulation import Simulation
from visualizer import DroneVisualizer


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <caminho_do_mapa> [--visual]")
        sys.exit(1)

    map_path = sys.argv[1]
    visual_mode = "--visual" in sys.argv or "--gui" in sys.argv

    data = parse_config(map_path)

    hubs_list = data["hubs"]
    num_drones = data["nb_drones"]

    start_hub_name = next(h.name for h in hubs_list if h.hub_type == "start")
    end_hub_name = next(h.name for h in hubs_list if h.hub_type == "end")

    sim = Simulation(data, num_drones, start_hub_name, end_hub_name)

    visualizer = None
    if visual_mode:
        visualizer = DroneVisualizer(data)

        sim.visualizer = visualizer

    sim.run()

    if visual_mode and visualizer:
        print(
            "\n🏁 Simulação concluída! Fecha a janela gráfica para terminar."
        )
        visualizer.root.mainloop()


if __name__ == "__main__":
    main()
