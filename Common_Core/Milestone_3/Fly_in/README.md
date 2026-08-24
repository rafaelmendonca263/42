*This project has been created as part of the 42 curriculum by rmedonca.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![School](https://img.shields.io/badge/School-42-black)
![Build](https://img.shields.io/badge/Build-Makefile-orange)
![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green)
![Type Checking](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet)
![Algorithm](https://img.shields.io/badge/Algorithm-Space--Time%20A*-yellow)
![UI](https://img.shields.io/badge/UI-Pygame%20%7C%20Terminal-red)
![Status](https://img.shields.io/badge/Status-Completed-success)

# Fly-in

## Description

Fly-in is a multi-drone simulation and routing project designed to model a constrained network of hubs and connections. Each drone must reach a destination while respecting the state of the network at every turn: hub capacities, link capacities, restricted zones, priority zones, and temporal conflicts.

The project is built around a graph-based environment where movement is not simply a shortest-path problem. A route is only valid if it respects the reservations made for hubs and corridors over time. This transforms the problem into a space-time scheduling challenge, where both the location and the turn index determine whether a move is feasible.

The system reads custom map files, validates them, schedules drone movements, and simulates their progression until all drones have reached the end hub. It also includes a visual representation that makes the global behavior of the system easier to understand and debug.

---

## Algorithm and implementation strategy

The project relies on a reservation-based planner inspired by A* search but adapted to time-aware routing.

### Graph model

The world is represented as an undirected graph:
- hubs are nodes,
- connections are edges,
- each hub may accept only a limited number of drones at the same time,
- each connection may carry only a limited number of simultaneous crossings.

### Route planning

Instead of computing a single static path, the planner builds a schedule as a sequence of states `(hub, turn)`. For each drone, a candidate move is accepted only if:
- the destination hub is available at arrival time,
- the connecting edge is free during the move,
- the zone type does not impose an invalid condition,
- the reservation table shows that no conflict occurs.

This reservation table is central to the project. It stores the occupancy of hubs and links at each turn and prevents collisions, bottlenecks, and invalid simultaneous use.

### Zone handling

The project supports several hub states and routing constraints:
- `normal`: standard movement,
- `priority`: preferred route, typically favored by the planner,
- `restricted`: slower or more constrained movement,
- `blocked`: not traversable,
- `max_drones`: hub limit,
- connection limits also controlled by capacity metadata.

### Validation layer

Before simulation starts, the parser validates:
- the presence of `nb_drones`,
- the syntax of every command,
- uniqueness and validity of start and end hubs,
- coordinate correctness,
- metadata consistency,
- graph feasibility and path existence.

The goal of this validation layer is to reject malformed or logically inconsistent maps before execution begins.

---

## Visual representation

The project includes a visualizer built with Pygame and a terminal-based output mode.

The visual component displays:
- hubs and connections on a graph,
- drones moving across the network,
- capacity usage and congestion,
- waiting behavior when a route is temporarily blocked,
- the final state of the fleet at destination.

This helps users understand why a route was chosen, where bottlenecks occur, and how the shared reservation system affects the global flow. In other words, the visualizer is not only for presentation: it is also a debugging and analysis tool that makes simulation behavior easier to interpret.

---

## Instructions

### Requirements

- Python 3.10 or higher
- `make`
- `venv` support

### Installation

From the project root, run:

```bash
make install
```

This creates a local virtual environment and installs the dependencies required for the project, including `pygame`, `mypy`, and `flake8`.

### Running the simulation

To run the project with a map file:

```bash
make run maps/easy/01_linear_path.txt
```

To launch the graphical visualizer:

```bash
.venv/bin/python main.py maps/easy/01_linear_path.txt --visual
```

To run the project in debug mode:

```bash
make debug maps/easy/01_linear_path.txt
```

### Static analysis and cleanup

```bash
make lint
```

Typical cleanup commands:

```bash
make clean
make fclean
```

---

## Project structure

```text
.
├── main.py              # entry point
├── parser.py            # map parsing and validation
├── pathfinder.py        # space-time scheduling logic
├── reservation.py       # reservation table for hubs and links
├── simulation.py        # main simulation loop
├── structure.py         # dataclasses for hubs, connections and drones
├── visualizer.py        # graphical rendering
├── network.py           # network-related helpers
├── Makefile             # installation and execution commands
├── maps/                # challenge maps
├── README.md            # documentation
└── .venv/               # generated virtual environment
```

---

## Example input

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [zone=priority]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

## Expected output

A successful simulation should complete without capacity violations and should show the drones advancing through the network turn by turn.

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

This illustrates the expected behavior: all drones reach the destination while respecting the reservation system and avoiding invalid simultaneous occupancy.

---

## Resources

### References

- A* Search Algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm
- Red Blob Games — A* tutorial: https://www.redblobgames.com/pathfinding/a-star/introduction.html
- Graph theory overview: https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)
- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/

### AI usage

AI tools were used only to improve the clarity and quality of the project documentation and communication.

Their usage was limited to:
- refining the README structure and wording,
- clarifying technical explanations,
- checking that the documentation matches the actual implementation,
- helping summarize the algorithm and project behavior in English.

The core algorithm design, graph modeling, reservation logic, parsing strategy, and validation mechanisms were developed and verified by the project author. AI was used as a support tool for explanation and documentation, not as a replacement for the technical implementation itself.

---

## Conclusion

Fly-in is a graph-based multi-drone simulation project focused on constrained path planning under temporal and capacity restrictions. It brings together parsing, validation, scheduling, reservation management, and visualization into a single system designed to challenge route planning in realistic congestion scenarios.
