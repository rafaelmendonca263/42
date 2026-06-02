import sys
import time
from parser import parse_config
from simulation import Simulation
from visualizer import DroneVisualizer

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <caminho_do_mapa> [--visual]")
        sys.exit(1)
        
    map_path = sys.argv[1]
    visual_mode = "--visual" in sys.argv or "--gui" in sys.argv
    
    # 1. Faz o parse do mapa
    data = parse_config(map_path)
    
    hubs_list = data["hubs"]
    num_drones = data["nb_drones"]
    
    start_hub_name = next(h.name for h in hubs_list if h.hub_type == "start")
    end_hub_name = next(h.name for h in hubs_list if h.hub_type == "end")
    
    # 2. Instancia a simulação SEM a flag visual para não quebrar o teu construtor
    sim = Simulation(data, num_drones, start_hub_name, end_hub_name)
    
    # 3. Inicializa o visualizador gráfico se a flag estiver ativa
    visualizer = None
    if visual_mode:
        visualizer = DroneVisualizer(data)
    
    # 4. Execução Controlada Turno a Turno (Se a tua classe Simulation permitir)
    # Nota: Se o teu método sim.run() correr tudo até ao fim de uma assentada,
    # teremos de injetar a atualização lá dentro. Mas se sim.run() aceitar um loop externo:
    
    # Caso o teu sim.run() corra tudo de forma automática, vamos usar o gancho abaixo.
    # Como o teu output de texto é impresso turno a turno, se o visualizer estiver ativo,
    # vamos interceptar o estado. 
    
    # Para garantir o funcionamento sem alterar o simulation.py, vamos fingir que o sim.run()
    # sabe que o visualizer existe injetando-o dinamicamente:
    if visual_mode:
        sim.visualizer = visualizer
        # Injetamos uma propriedade na classe para o teu loop interno usar, se necessário.
    
    sim.run()
    
    # Mantém a janela gráfica aberta no fim da simulação
    if visual_mode and visualizer:
        print("\n🏁 Simulação concluída! Fecha a janela gráfica para terminar.")
        visualizer.root.mainloop()

if __name__ == "__main__":
    main()