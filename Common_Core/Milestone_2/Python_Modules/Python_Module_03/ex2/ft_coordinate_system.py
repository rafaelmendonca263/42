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
    except Exception as e:
        print(f"Error parsing coordinates: {e}")
        print(
            f"Error details - Type: {type(e).__name__}, "
            f"Args: {e.args}"
        )
        return None


if __name__ == "__main__":
    print("=== Game Coordinate System ===")

    origin = (0, 0, 0)

    position = (10, 20, 5)
    print(f"Position created: {position}")

    dist = distance_3d(origin, position)
    print(
        f"Distance between {origin} and {position}: "
        f"{dist:.2f}"
    )

    coord_str = "3,4,0"
    parsed = parse_coordinates(coord_str)
    if parsed is not None:
        print(f"Parsed position: {parsed}")
        dist = distance_3d(origin, parsed)
        print(
            f"Distance between {origin} and {parsed}: "
            f"{dist}"
        )

    invalid_str = "abc,def,ghi"
    print(f'Parsing invalid coordinates: "{invalid_str}"')
    parse_coordinates(invalid_str)

    print("Unpacking demonstration:")
    x, y, z = parsed
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")