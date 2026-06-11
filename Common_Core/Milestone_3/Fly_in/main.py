import sys
from parser import parse_config
from network import NetworkGraph
from simulation import Simulation

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <caminho_do_mapa> [--visual]")
        sys.exit(1)
        
    map_path = sys.argv[1]
    visual_mode = "--visual" in sys.argv or "--gui" in sys.argv

    data = parse_config(map_path)

    graph = NetworkGraph(data)

    hubs_list = data["hubs"]
    num_drones = data["nb_drones"]
    
    start_hub_name = next(h.name for h in hubs_list if h.hub_type == "start")
    end_hub_name = next(h.name for h in hubs_list if h.hub_type == "end")

    sim = Simulation(graph, num_drones, start_hub_name, end_hub_name, visual=visual_mode)

    sim.run()

    if visual_mode and hasattr(sim, 'visualizer'):
        print("\n🏁 Simulação concluída! Fecha a janela gráfica para terminar.")
        sim.visualizer.root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)