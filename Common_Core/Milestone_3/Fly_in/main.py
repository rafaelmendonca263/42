"""Ponto de entrada do simulador Fly-in."""

import sys
import argparse
from parser import parse_map_file, ParseError
from simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulador de Drones Fly-in")
    parser.add_argument("map_file", help="Caminho para o ficheiro do mapa")
    parser.add_argument(
        "--visual", action="store_true", help="Ativar representação visual"
    )
    args = parser.parse_args()

    try:
        parsed_data = parse_map_file(args.map_file)
        sim = Simulation(parsed_data, visual=args.visual)
        sim.run()  # O sim.run() deve imprimir os turnos diretamente na consola (print)

    except ParseError as pe:
        print(f"Erro de Parsing: {pe}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro de execução: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()