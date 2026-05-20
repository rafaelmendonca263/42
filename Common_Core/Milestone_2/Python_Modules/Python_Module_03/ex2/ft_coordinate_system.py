import math


def distance_3d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def parse_coordinates(coord_str):
    print(f'Parsing coordinates: "{coord_str}"')
    try:
        parts = coord_str.split(",")

        if len(parts) != 3:
            raise ValueError

        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])
        return (x, y, z)
    except ValueError:
        print("Invalid syntax")
        exit(1)
    except IndexError:
        print("Invalid syntax")
        exit(1)


if __name__ == "__main__":
    try:
        print("=== Game Coordinate System ===\n")

        print("Get a first set of coordinates")

        origin = None
        first_coordenates = None
        second_coordenates = None

        while first_coordenates is None:
            origin = input(
                "Enter new coordinates as " "floats in format 'x,y,z': "
            )
            first_coordenates = parse_coordinates(origin)
            print(
                f"Got a first tuple: ({first_coordenates[0]},"
                f" {first_coordenates[1]}, {first_coordenates[2]})"
            )
            print(
                f"It includes: X={first_coordenates[0]}, "
                f"Y={first_coordenates[1]}, Z={first_coordenates[2]}"
            )
            print(
                "Distance to center: "
                f"{distance_3d((0, 0, 0), (first_coordenates))}"
            )

        print("\nGet a second set of coordinates")

        while second_coordenates is None:
            origin = input(
                "Enter new coordinates as floats " "in format 'x,y,z': "
            )
            second_coordenates = parse_coordinates(origin)
            print(
                "Distance between the 2 sets of coordinates: "
                f"{distance_3d((second_coordenates), (first_coordenates))}"
            )

    except Exception as e:
        print(e)
        exit(1)
