from collections.abc import Callable
from mazegen import MazeGenerator


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

RESET = "\033[0m"


class Display_Maze:
    def __init__(
        self,
        maze: MazeGenerator,
        solver: Callable[[], list[str]],
    ) -> None:
        self.maze = maze
        self.solver = solver

    def build_path_coords(self, directions: list[str]) -> set[tuple[int, int]]:
        x, y = self.maze.entry
        path: list[tuple[int, int]] = [(x, y)]

        for d in directions:
            if d == "N":
                y -= 1
            elif d == "S":
                y += 1
            elif d == "E":
                x += 1
            elif d == "W":
                x -= 1

            path.append((x, y))
        return set(path)

    def display(self, show_path: bool = False,
                change_color: bool = False) -> None:
        directions = self.solver()
        path_coords = self.build_path_coords(directions)

        for row in self.maze.grid:
            print(self.upper_line(row, change_color))
            print(self.middle_line(row, path_coords, show_path, change_color))
        print(self.lower_line(self.maze.grid[-1], change_color))

    def upper_line(self, row: list["MazeGenerator.Cell"],
                   change_color: bool = False) -> str:
        if not change_color:
            line = f"{BRIGHT_WHITE}+{RESET}"
            for cell in row:
                line += (f"{BRIGHT_WHITE}---+{RESET}"
                         if cell.direction["N"]
                         else f"{BRIGHT_WHITE}   +{RESET}")
            return line
        line = f"{BRIGHT_GREEN}+{RESET}"
        for cell in row:
            line += (f"{BRIGHT_GREEN}---+{RESET}"
                     if cell.direction["N"]
                     else f"{BRIGHT_GREEN}   +{RESET}")
        return line

    def middle_line(self, row: list["MazeGenerator.Cell"],
                    path_coords: set[tuple[int, int]],
                    show_path: bool = False,
                    change_color: bool = False) -> str:

        entry = f"{GREEN}E{RESET}"
        exit = f"{RED}X{RESET}"
        path = f"{BG_BLUE} {RESET}"
        cell_close = f"{BG_MAGENTA} {RESET}"
        bar = f"{BRIGHT_WHITE}|{RESET}"
        if change_color:
            entry = f"{BRIGHT_RED}E{RESET}"
            exit = f"{MAGENTA}X{RESET}"
            path = f"{BG_BRIGHT_RED} {RESET}"
            cell_close = f"{BG_BRIGHT_YELLOW} {RESET}"
            bar = f"{BRIGHT_GREEN}|{RESET}"
        line = ""
        for cell in row:
            line += bar if cell.direction["W"] else " "
            if cell.entry:
                symbol = entry
            elif cell.exit:
                symbol = exit
            elif (cell.x, cell.y) in path_coords and show_path:
                symbol = path
            elif cell.closed:
                symbol = cell_close
            else:
                symbol = " "

            line += f" {symbol} "

        line += bar if row[-1].direction["E"] else " "
        return line

    def lower_line(self, row: list["MazeGenerator.Cell"],
                   change_color: bool = False) -> str:
        if not change_color:
            line = f"{BRIGHT_WHITE}+{RESET}"
            for cell in row:
                line += (f"{BRIGHT_WHITE}---+{RESET}"
                         if cell.direction["S"]
                         else f"{BRIGHT_WHITE}   +{RESET}")
            return line
        line = f"{BRIGHT_GREEN}+{RESET}"
        for cell in row:
            line += (f"{BRIGHT_GREEN}---+{RESET}"
                     if cell.direction["S"]
                     else f"{BRIGHT_GREEN}   +{RESET}")
        return line
