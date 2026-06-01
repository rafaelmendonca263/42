"""
MazeGenerator – Reusable Maze Generation Module
==============================================

This module provides the MazeGenerator class used in the A‑Maze‑Ing project.
It is a standalone, importable maze generator suitable for packaging as
mazegen-* and installation via pip. The generator supports configurable size,
entry/exit coordinates, perfect/non‑perfect generation, optional random seed,
and exposes both the internal maze structure and a shortest‑path solution.

Basic Usage
-----------

    from mazegen import MazeGenerator

    mg = MazeGenerator(
        height=10,             # Maze generation (DFS)
        width=10,
        entry=(0, 0),
        exit=(9, 9),
        output_file="maze.txt",
        perfect=True,
        seed=42
    )
    maze = mg.get_maze()       # Internal structure
    path = mg.get_path()       # Shortest path (BFS)

Parameters
----------

height : int
    Number of rows in the maze.
width : int
    Number of columns in the maze.
entry : (int, int)
    Starting cell coordinates (x, y).
exit : (int, int)
    Ending cell coordinates (x, y).
output_file : str
    File where the hexadecimal maze representation is written.
perfect : bool
    If True, the maze contains no cycles.
seed : int, optional
    Optional seed for reproducible maze generation.

Public Methods
--------------

get_maze()
    Returns the internal maze representation.
get_solution()
    Returns the shortest path from entry to exit (computed via BFS).

Notes
-----

• This module only provides reusable generation and solving logic.
  Rendering, ASCII display, configuration parsing, and direction output
  belong to the main A‑Maze‑Ing project.

• The internal structure format does not need to match the output file format.
"""
import random
from collections import deque
from typing import Deque, Any
from typing import TypedDict


class MazeConfig(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    SEED: int
    OUTPUT_FILE: str


class MazeGenerator:
    class Cell:
        def __init__(self, y: int, x: int, y_len: int, x_len: int) -> None:
            self.direction = {
                        "N": 1,
                        "E": 1,
                        "S": 1,
                        "W": 1}
            self.maze_limit = {
                        "N": 0,
                        "E": 0,
                        "S": 0,
                        "W": 0}
            self.x = x
            self.y = y
            self.visited = False
            self.entry = False
            self.exit = False
            self.closed = False
            if y == 0:
                self.maze_limit["N"] = 1
            if y == y_len - 1:
                self.maze_limit["S"] = 1
            if x == 0:
                self.maze_limit["W"] = 1
            if x == x_len - 1:
                self.maze_limit["E"] = 1

        def __repr__(self) -> str:
            return f"C({self.x},{self.y})"

    def __init__(self, config: MazeConfig) -> None:
        random.seed(config["SEED"])
        self.config = config
        self.height = config["HEIGHT"]
        self.width = config["WIDTH"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        self.grid_creator()
        self.fourty_two()

        self.dfs_backtracing(self.entry[0], self.entry[1], perfect=True)

        if not self.perfect:
            while not self.has_multiple_paths():
                self.make_imperfect(extra_paths=1)

        self.output_hex()
        sv = self.SolveMaze(self, config)
        self.path = sv.solve_maze()

    def close_cell(self, y: int, x: int) -> None:
        if self.grid[y][x].entry or self.grid[y][x].exit:
            print("Error: The coordinades of entry and"
                  " exit cannot be in a closed cell.")
            exit(1)
        self.grid[y][x].maze_limit.update({"N": 1, "E": 1, "S": 1, "W": 1})
        self.grid[y - 1][x].maze_limit["S"] = 1
        self.grid[y + 1][x].maze_limit["N"] = 1
        self.grid[y][x + 1].maze_limit["W"] = 1
        self.grid[y][x - 1].maze_limit["E"] = 1
        self.grid[y][x].closed = True

    def grid_creator(self) -> list[list[Cell]]:
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.Cell(y, x, self.height, self.width))
            grid.append(row)
        self.grid = grid
        self.define_entry(self.entry[0], self.entry[1])
        self.define_exit(self.exit[0], self.exit[1])
        return grid

    def define_entry(self, x: int, y: int) -> None:
        self.grid[y][x].entry = True
        self.grid[y][x].visited = True

    def define_exit(self, x: int, y: int) -> None:
        self.grid[y][x].exit = True

    def remove_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        if x == nx and y > ny:
            self.grid[y][x].direction["N"] = 0
            self.grid[ny][nx].direction["S"] = 0
        elif x == nx and y < ny:
            self.grid[y][x].direction["S"] = 0
            self.grid[ny][nx].direction["N"] = 0
        elif y == ny and x < nx:
            self.grid[y][x].direction["E"] = 0
            self.grid[ny][nx].direction["W"] = 0
        elif y == ny and x > nx:
            self.grid[y][x].direction["W"] = 0
            self.grid[ny][nx].direction["E"] = 0

    def dfs_backtracing(self, x: int, y: int, perfect: bool = True) -> None:
        self.grid[y][x].visited = True
        directions = ["N", "E", "S", "W"]
        probably = 0.04
        if self.height < 13 and self.width < 13:
            probably = 0.10
        try:
            while (True):
                if len(directions) == 0:
                    return
                dir = random.choice(directions)
                directions.remove(dir)
                if dir == "N" and not self.grid[y][x].maze_limit["N"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x, y - 1)
                        if not self.grid[y - 1][x].visited:
                            self.dfs_backtracing(x, y - 1, False)
                            self.remove_wall(x, y, x, y - 1)

                    elif not self.grid[y - 1][x].visited:
                        self.remove_wall(x, y, x, y - 1)
                        self.dfs_backtracing(x, y - 1)

                elif dir == "E" and not self.grid[y][x].maze_limit["E"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x + 1, y)
                        if not self.grid[y][x + 1].visited:
                            self.dfs_backtracing(x + 1, y, False)
                            self.remove_wall(x, y, x + 1, y)

                    elif not self.grid[y][x + 1].visited:
                        self.remove_wall(x, y, x + 1, y)
                        self.dfs_backtracing(x + 1, y)

                elif dir == "S" and not self.grid[y][x].maze_limit["S"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x, y + 1)
                        if not self.grid[y + 1][x].visited:
                            self.dfs_backtracing(x, y + 1, False)
                            self.remove_wall(x, y, x, y + 1)

                    elif not self.grid[y + 1][x].visited:
                        self.remove_wall(x, y, x, y + 1)
                        self.dfs_backtracing(x, y + 1)

                elif dir == "W" and not self.grid[y][x].maze_limit["W"]:
                    if not perfect:
                        if random.random() < probably:
                            self.remove_wall(x, y, x - 1, y)
                        if not self.grid[y][x - 1].visited:
                            self.dfs_backtracing(x - 1, y, False)
                            self.remove_wall(x, y, x - 1, y)

                    elif not self.grid[y][x - 1].visited:
                        self.remove_wall(x, y, x - 1, y)
                        self.dfs_backtracing(x - 1, y)
        except Exception:
            self.dfs_backtracing(x, y, perfect)

    def make_imperfect(self, extra_paths: int = 1) -> None:
        walls_removed = 0
        max_attempts = self.width * self.height * 2
        attempts = 0

        while walls_removed < extra_paths and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            dirs = ["N", "E", "S", "W"]
            valid_dirs = [
                          d for d in dirs
                          if not self.grid[y][x].maze_limit[d]
                          and not self.grid[y][x].closed
                ]

            if not valid_dirs:
                continue

            d = random.choice(valid_dirs)

            if self.grid[y][x].direction[d] == 1:
                if d == "N":
                    self.remove_wall(x, y, x, y - 1)
                elif d == "E":
                    self.remove_wall(x, y, x + 1, y)
                elif d == "S":
                    self.remove_wall(x, y, x, y + 1)
                elif d == "W":
                    self.remove_wall(x, y, x - 1, y)
                walls_removed += 1

    def has_multiple_paths(self) -> bool:
        entry_pos = self.entry
        exit_pos = self.exit
        paths_found = 0
        visited = set()

        def dfs_search(current_pos: tuple[int, int]) -> None:
            nonlocal paths_found
            if paths_found >= 2:
                return

            if current_pos == exit_pos:
                paths_found += 1
                return

            visited.add(current_pos)

            neighbors = self.SolveMaze.get_neighbors(current_pos, self)

            for direction, neighbor_pos in neighbors:
                if neighbor_pos not in visited:
                    dfs_search(neighbor_pos)

            visited.remove(current_pos)

        dfs_search(entry_pos)
        return paths_found >= 2

    def fourty_two(self) -> None:
        y = int(self.height / 2)
        x = int(self.width / 2)
        self.close_cell(y, x - 1)
        self.close_cell(y, x - 2)
        self.close_cell(y, x - 3)

        self.close_cell(y, x - 3)
        self.close_cell(y - 1, x - 3)
        self.close_cell(y - 2, x - 3)

        self.close_cell(y, x - 1)
        self.close_cell(y + 1, x - 1)
        self.close_cell(y + 2, x - 1)

        self.close_cell(y, x + 1)
        self.close_cell(y, x + 2)
        self.close_cell(y, x + 3)

        self.close_cell(y, x + 3)
        self.close_cell(y - 1, x + 3)
        self.close_cell(y - 2, x + 3)

        self.close_cell(y - 2, x + 1)
        self.close_cell(y - 2, x + 2)
        self.close_cell(y - 2, x + 3)

        self.close_cell(y, x + 1)
        self.close_cell(y + 1, x + 1)
        self.close_cell(y + 2, x + 1)

        self.close_cell(y + 2, x + 1)
        self.close_cell(y + 2, x + 2)
        self.close_cell(y + 2, x + 3)

    def output_hex(self) -> None:
        binarie = ""
        output = ""
        for row in self.grid:
            for cell in row:
                binarie = (str(cell.direction["N"]) +
                           str(cell.direction["E"]) +
                           str(cell.direction["S"]) +
                           str(cell.direction["W"])
                           )
                output += hex(int(binarie, 2))[2:].upper()
            output += '\n'
        output += f"\n{self.entry[0]}, {self.entry[1]}"
        output += f"\n{self.exit[0]}, {self.exit[1]}\n"
        with open(self.output_file, "w") as f:
            f.write(output)

    def get_path(self) -> list[str]:
        return self.path

    def get_maze(self) -> list[list[Cell]]:
        return self.grid

    class SolveMaze:
        def __init__(self, maze: "MazeGenerator", config: MazeConfig) -> None:
            self.maze = maze
            self.config = config
            self.grid: list[list[MazeGenerator.Cell]] = maze.grid
            self.dfs_backtracing: Any = maze.dfs_backtracing

        @staticmethod
        def get_neighbors(
            position: tuple[int, int],
            maze: 'MazeGenerator'
        ) -> list[tuple[str, tuple[int, int]]]:

            x, y = position
            cell = maze.grid[y][x]
            directions: list[tuple[str, tuple[int, int]]] = []

            if cell.direction["N"] == 0:
                directions.append(("N", (x, y - 1)))
            if cell.direction["E"] == 0:
                directions.append(("E", (x + 1, y)))
            if cell.direction["S"] == 0:
                directions.append(("S", (x, y + 1)))
            if cell.direction["W"] == 0:
                directions.append(("W", (x - 1, y)))

            valid_neighbors: list[tuple[str, tuple[int, int]]] = []
            for direction, (nx, ny) in directions:
                if 0 <= nx < maze.width and 0 <= ny < maze.height:
                    valid_neighbors.append((direction, (nx, ny)))

            return valid_neighbors

        def solve_maze(self) -> list[str]:
            entry: tuple[int, int] = self.config["ENTRY"]
            exit: tuple[int, int] = self.config["EXIT"]

            queue: Deque[tuple[tuple[int, int], list[str]]] = deque()
            queue.append((entry, []))

            visited: set[tuple[int, int]] = {entry}

            while queue:
                current_position, path = queue.popleft()

                if current_position == exit:
                    return path

                for direction, neighbor in self.get_neighbors(current_position,
                                                              self.maze):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [direction]))

            return []

        @staticmethod
        def build_path_coords(
            entry: tuple[int, int],
            directions: list[str]
        ) -> set[tuple[int, int]]:

            x, y = entry
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

        def write_solution(self) -> None:
            path = self.solve_maze()
            solution = "".join(path) if path else ""

            with open(self.config["OUTPUT_FILE"], "a") as f:
                f.write(solution)

        def find_paths(self, x: int, y: int, path: list[str]) -> None:
            self.grid[y][x].visited = True
            directions = ["N", "E", "S", "W"]

            while True:
                if self.grid[y][x].exit:
                    return

                if not directions:
                    return

                dir_choice = random.choice(directions)
                directions.remove(dir_choice)

                if dir_choice == "N" and not self.grid[y][x].direction["N"]:
                    if not self.grid[y - 1][x].visited:
                        path.append("N")
                        self.dfs_backtracing(x, y - 1, path)

                elif dir_choice == "E" and not self.grid[y][x].direction["E"]:
                    if not self.grid[y][x + 1].visited:
                        path.append("E")
                        self.dfs_backtracing(x + 1, y, path)

                elif dir_choice == "S" and not self.grid[y][x].direction["S"]:
                    if not self.grid[y + 1][x].visited:
                        path.append("S")
                        self.dfs_backtracing(x, y + 1, path)

                elif dir_choice == "W" and not self.grid[y][x].direction["W"]:
                    if not self.grid[y][x - 1].visited:
                        path.append("W")
                        self.dfs_backtracing(x - 1, y, path)
