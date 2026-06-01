*This project has been created as part of the 42 curriculum by dosorio-, rmedonca.*

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Build](https://img.shields.io/badge/Build-Makefile-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green)
![Typing](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet)
![Algorithms](https://img.shields.io/badge/Algorithms-DFS%20%7C%20BFS-yellow)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)
![Language](https://img.shields.io/badge/Language-Python-blue)

# Description

---

This project implements a fully configurable **maze generator and solver**, capable of producing valid mazes based on a user-defined configuration file. The program reads the configuration, validates all parameters, generates the maze, solves it, and outputs the result.

The focus is on **procedural generation**, **clean modular design**, and **reusable components**.

# Features

- Configurable maze generation
- Randomized maze generation
- Shortest-path solving using BFS
- ASCII terminal visualization
- Output file containing solution directions

---

## Preview

Example of generated maze:
```
+---+---+---+
| E   *   * |
+   +---+   +
|   |     x |
+---+-------+
```

# Instructions

## Installation

The project uses a **Python virtual environment** managed through a Makefile.

To install all dependencies and prepare the environment, run:

```
make install
```

This will:
- Create a virtual environment (`venv/`) if it does not exist  
- Upgrade `pip`  
- Install development tools:
  - `flake8`
  - `mypy`

> Note: The project has no external runtime dependencies.

---

## Running the Program

To generate and solve a maze using the default configuration file:

```
make run
```

This executes:

```
python3 a_maze_ing.py config.txt
```

## Debug Mode

To run the program using the Python debugger:

```
make debug
```

## Cleaning Temporary Files

To remove caches and temporary Python files:

```
make clean
```

This deletes:
- `__pycache__/`
- `.mypy_cache/`
- `.pyc` files

## Linting and Static Analysis

To check code style and typing:

```
make lint
```

To run strict linting and typing rules:

```
make lint-strict
```

# Config File Structure

The configuration file must follow this format:

```
WIDTH=<int>
HEIGHT=<int>
ENTRY=x,y
EXIT=x,y
OUTPUT_FILE=string.txt
PERFECT=bool
```
## Example

```
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=output.txt
PERFECT=True
```

### Field descriptions

- **WIDTH / HEIGHT** — Maze dimensions
- **ENTRY** — Starting position
- **EXIT** — Ending position
- **OUTPUT_FILE** — File where the maze data is saved, including:
  - Maze representation in hexadecimal
  - Solution path (N, S, E, W)
  - Entry coordinates
  - Exit coordinates
- **PERFECT** — If True, the maze has no cycles (only one unique path between any two points)

---

# Output Format

The output file contains:

- Maze representation in hexadecimal format  
- Entry coordinates  
- Exit coordinates  
- Solution path as a sequence of directions  

## Directions

- N → North
- S → South
- E → East
- W → West

## Example

```
NSESEW
```

This represents the shortest path from ENTRY to EXIT.

---

# Maze Generation Algorithm

## Depth‑First Search (DFS) Backtracking

DFS Backtracking was chosen as the maze generation algorithm.

### Summary of the method
- Select an initial cell  
- Mark it as visited  
- Choose a random unvisited neighbor  
- Remove the wall between both cells  
- Move to the neighbor and repeat  
- Backtrack when no neighbors remain

### Why DFS

- Simple and intuitive  
- Produces long, interesting paths  
- Low computational cost  
- Easy to implement and adapt  

---

# Maze Solving Algorithm

## Breadth‑First Search (BFS)

BFS was used to solve the maze by finding the shortest possible path from the entry to the exit.

### How it works

- Starts from ENTRY  
- Explores neighbors level by level  
- Stores predecessors  
- Stops when EXIT is found  
- Reconstructs shortest path   

### Why BFS was chosen

- Guarantees shortest path  
- Efficient for grid-based problems  
- Deterministic and reliable  

---

# Algorithm Complexity

- DFS (Generation): **O(N)**  
- BFS (Solving): **O(V + E)**  

Both scale linearly with the number of cells.

---

# Project Structure

```
maze/
    generator.py
    solver.py

parsing/
    config_parser.py

output/
    display.py

a_maze_ing.py
Makefile
config.txt
```

---

# Reusable Code

## mazegen
- The entire Mazegenerator class with the nested SolveMaze class to resolve the Maze and the Cell class to represents a cell.



### How to reuse the code?
- **Install the build if you hasn't installed with:**  
pip install build  

- **Then executes the build:**  
python3 -m build

- **The build will make two files:**   
mazegen-1.0.0.tar.gz and mazegen-1.0.0-py3-none-any.whl

- **To install the mazegen module enter:**  
pip install mazegen-1.0.0-py3-none-any.whl

- **And to extract(view) the module files enter:**  
tar -xzf mazegen-1.0.0.tar.gz 

# Testing

The project was manually tested to ensure:
- Invalid configurations  
- Boundary conditions  
- Different maze sizes  
- Entry/Exit edge cases  

Frameworks like `pytest` can be used but are not included.

---

# .gitignore

The project includes a `.gitignore` file excluding:

- `venv/`  
- `__pycache__/`  
- `*.pyc`  
- `.mypy_cache/`  

---

# Team and Project Management

## Team Members

### dosorio-
**Roles:**
- DFS algorithm implementation  
- Grid structure and cell manipulation  
- Terminal visualization  
- Documentation  
- Output file generation (maze seed, shortest path, status)  

### rmedonca
**Roles:**
- Configuration parser implementation  
- Terminal display  
- BFS algorithm implementation for maze solving  
- Project organization and structure  
- Flake8 compliance

---

# Resources

## References

- Red Blob Games — Maze generation algorithms  
- DFS, BFS, and backtracking articles  

## Use of AI

AI was used strictly as an auxiliary tool for:
- Improving technical explanations  
- Generating documentation examples  
- Suggesting modular organization  
- Reviewing the README text  

All code was written manually.