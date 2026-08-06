*This project has been created as part of the 42 curriculum by <rmedonca>.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![School](https://img.shields.io/badge/School-42-black)
![Build](https://img.shields.io/badge/Build-Makefile-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green)
![Type Checking](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet)
![Algorithm](https://img.shields.io/badge/Algorithm-Space--Time%20A*-yellow)
![UI](https://img.shields.io/badge/UI-Pygame%20%7C%20Terminal-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

# Fly-in — Drone Fleet Pathfinding & Simulation

## Description

**Fly-in** is an algorithmic simulation engine designed to coordinate and optimize the navigation of multiple drones through a complex, spatial graph of interconnected hubs (zones) and air corridors (connections). The primary goal is to route all drones from a designated `start_hub` to an `end_hub` in the minimal number of simulation turns while satisfying real-time space-time capacity constraints.

Key features of the simulator include:
- **Space-Time Pathfinding (A*)**: Calculates conflict-free routes across spatial nodes and time dimensions, avoiding node and link capacity bottlenecks.
- **Dynamic Capacity Management**: Supports node capacities (`max_drones`) and corridor link capacities (`max_link_capacity`).
- **Zone Mechanics**: Handles varying cost and transition dynamics across zone types:
  - `normal`: 1 turn traversal cost.
  - `priority`: 1 turn cost, prioritized during route optimization.
  - `restricted`: 2 turns transition (1 turn on connection link + 1 turn to land on hub).
  - `blocked`: Inaccessible zones.
- **Strict Parsing & Validation**: Validates map syntax, coordinates, node naming (dashes disallowed), and logical consistency.
- **Real-Time Visualization**: Powered by Pygame to render drone movements, hub capacities, and zone types visually.

---

## Architecture & Algorithm Design

### 1. Reservation Table & Space-Time A*
Unlike standard pathfinding (which only considers 2D/3D spatial coordinates), Fly-in handles multi-drone interaction over time. The **SpaceTimeAStar** pathfinder uses a shared `ReservationTable`:
- Nodes and connections are reserved at specific discrete time steps `(location, time)`.
- Drones can perform waiting maneuvers (staying at a hub) if a downstream corridor or destination hub is temporarily saturated.
- Route planning is executed iteratively for each drone and committed to the central space-time schedule to prevent mid-air collisions or capacity overfills.

### 2. Immediate Capacity Liberation
The simulation engine processes turns dynamically: as a drone departs a hub during a turn, it frees capacity for another drone arriving in that same turn, ensuring optimal throughput without overstepping capacity limits.

---

## Instructions

### Prerequisites
- Python 3.10 or higher
- `virtualenv` / `venv` support

### Building & Running via Makefile

The project includes a fully featured `Makefile` to handle environment setup, dependencies, linting, and execution.

1. **Install Dependencies**
   Creates a `.venv` virtual environment and installs required packages (`pygame`, `mypy`, `flake8`):
   ```
   make install
   ```

2. **Run the Simulation**
    Execute the simulation with a map file. The --visual flag activates the graphical interface:
    ```
    make run maps/example_map.txt
    ```
    Or execute directly with Python:
    ```
    .venv/bin/python main.py maps/example_map.txt --visual
    ```

3. **Debug Mode**
    Runs the program using the built-in Python debugger (pdb):
    ```
    make debug maps/example_map.txt
    ```

4. **Code Quality & Type Checking**
    Runs flake8 and mypy with strict type checks required by the 42 standard:
    ```
    make lint
    ```

5. **Clean Up**
    Removes caches and build artifacts:
    ```
    make clean
    # Or remove the .venv completely:
    make fclean
    ```

## Map File Format Example
```
    nb_drones: 3
    start_hub: roof1 0 0 [max_drones=5]
    hub: corridorA 10 0 [zone=priority max_drones=2]
    hub: bridge1 20 0 [zone=restricted max_drones=1]
    end_hub: zoneEnd 30 0 [max_drones=5]

    connection: roof1-corridorA [max_link_capacity=2]
    connection: corridorA-bridge1
    connection: bridge1-zoneEnd
```

## Resources & Artificial Intelligence (AI) Usage
In compliance with 42 curriculum guidelines regarding AI assistance:

**AI Collaboration:** Generative AI tools (ChatGPT/Gemini) were used during the project as a pair-programming partner.

**Tasks Assisted by AI:**

- Refining edge-case handling in syntax parsing (e.g., verifying dash prohibitions in hub names and validating enum values for zone types).

- Structuring type annotations (mypy) and enforcing PEP-8 compliance (flake8).

- Formatting project documentation (README.md).

**Core Implementation:** All algorithms (Space-Time A*, Graph Representation, Reservation System, Simulation Engine) were studied, designed, and verified by the author.