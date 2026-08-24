
import os
import sys
import argparse
from parser import parse_map_file, ParseError
from simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Fly-in Drone Simulator")
    parser.add_argument("map_file", help="path to the map file")
    parser.add_argument("--visual", action="store_true")
    args = parser.parse_args()

    if (
        not os.path.isfile(args.map_file)
        or not os.access(args.map_file, os.R_OK)
    ):
        parser.error(
            f"map file not found or not readable: {args.map_file}"
        )

    try:
        parsed_data = parse_map_file(args.map_file)
        sim = Simulation(parsed_data, visual=args.visual)
        sim.run()

    except ParseError as e:
        print(f"Parsing Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Execution error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
