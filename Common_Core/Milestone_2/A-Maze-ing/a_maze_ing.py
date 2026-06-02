from parsing.config_parser import ConfigParser
from mazegen import MazeGenerator, MazeConfig
from output.display import (Display_Maze, BRIGHT_GREEN,
                            BRIGHT_YELLOW, BRIGHT_RED, RESET)
import sys
import os
import random


def main(color: bool = False) -> None:
    try:
        os.system("clear")
        config_parser = ConfigParser(sys.argv[1])
        config: MazeConfig = config_parser.parse()
    except IndexError:
        print("ERROR: The program has to be executes: "
              "'python3 a_maze_ing.py config.txt'")
        exit(1)
    if not config.get("SEED"):
        config["SEED"] = random.randrange(2**32)

    maze = MazeGenerator(config)
    sv = MazeGenerator.SolveMaze(maze, config)
    display = Display_Maze(
        maze,
        sv.solve_maze,
    )
    display.display(False, color)
    sv.write_solution()
    show_hide = 2
    path = False
    while True:
        watermelon = f"{BRIGHT_RED}Watermelon{BRIGHT_GREEN}"
        theme = ""
        if color:
            theme = BRIGHT_GREEN
        print(f"{theme}╔═════════════════ Manual ══════════════════╗")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit\n")
        print("╔═════════════════ Status ══════════════════╗")
        print(f"  ==== Height: {config['HEIGHT']}, Width: {config['WIDTH']}")
        print(f"  ==== Entry: x({config['ENTRY'][0]}), y({config['ENTRY'][1]}"
              f") ││ Exit: x({config['EXIT'][0]}), y({config['EXIT'][1]})")
        print(f"  ==== Maze type: "
              f"{'Perfect Maze' if config['PERFECT'] else 'Imperfect Maze'}")
        print(f"  ==== Seed: {config['SEED']}")
        print(f"  ==== Current Theme: {watermelon if color else 'Normal'}")

        print("╚═══════════════════════════════════════════╝")
        choice = input("Choice? (1-4): ")
        if choice not in ("1", "2", "3", "4"):
            os.system("clear")
            display.display(path, color)
            print(f"{BRIGHT_YELLOW}\nError: Enter a number "
                  f"between 1 and 4!\n{RESET}")

        elif choice == "1":
            os.system("clear")
            main(color)
        elif choice == "2":
            os.system("clear")
            if show_hide % 2 != 0:
                path = False
                display.display(path, color)
            else:
                path = True
                display.display(path, color)
            show_hide += 1
        elif choice == "3":
            os.system("clear")
            color = not color
            display.display(path, color)
        elif choice == "4":
            exit(0)


if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("\nUser kill the program with EOF")
        exit(1)
