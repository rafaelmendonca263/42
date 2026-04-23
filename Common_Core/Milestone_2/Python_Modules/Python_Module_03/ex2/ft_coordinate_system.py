
import sys
import math


def distance_3d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2 +
        (z2 - z1) ** 2
    )


def parse_coordinates(coord_str):
    print(f'Parsing coordinates: "{coord_str}"')
    try:
        parts = coord_str.split(",")
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        return (x, y, z)
    except Exception:
        print("Invalid syntax")
        return None


if __name__ == "__main__":
    print("=== Game Coordinate System ===\n")

    print("Get a first set of coordinates")

    for first_cordenates is None:
    origin = input("Enter new coordinates as floats in format 'x,y,z': ")
    first_coordenates = parse_coordinates
    print(f"It includes: X={first_coordenates.x}, Y={first_coordenates.y}, Z={first_coordenates.z}")
    

    print("Get a second set of coordinates")
    origin = input("Enter new coordinates as floats in format 'x,y,z': ")