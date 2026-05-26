import sys
from structure import Hub, Connection


class ParseError(Exception):
    pass


def extract_info(filepath: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            hubs = []
            num = 0
            connections = []
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                part = line.split(":")
                type = part[0].strip()
                if type == "nb_drones":
                    num = int(part[1].strip())
                    continue
                elif type == "connection":
                    corredores = part[1].split("-")
                    corredor0 = corredores[0].strip()
                    corredor1 = corredores[1].strip()
                    if "[" in corredor0:
                        corredor0 = corredor0.split("[")[0].strip()
                    if "[" in corredor1:
                        corredor1 = corredor1.split("[")[0].strip()
                    connections.append(Connection(corredor0, corredor1))
                    continue
                else:
                    if "[" in part[1]:
                        data = part[1].split("[")
                        mandatory = data[0].strip()
                        metadata = data[1].strip()
                        metadata = metadata.rstrip("]")
                        coor = mandatory.split()
                    else:
                        data = part[1]
                        coor = data.split()
                    name = coor[0].strip()
                    x = int(coor[1])
                    y = int(coor[2])

                    hubs.append(Hub(name, x, y, "normal", None, 1))

        dict_hubs = {
            "hubs": hubs,
            "Connection": connections,
            "nb_drones": num
        }

        return dict_hubs

    except Exception as e:
        raise ParseError("Not expected error while extracting "
                         f"information: {e}")


def validate_metadata(metadata_str: str):
    allowed_keys = ["color=",
                    "max_drones=",
                    "zone=",
                    "max_drones=",
                    "max_link_capacity="]
    if not metadata_str:
        return

    pairs = metadata_str.split()
    for pair in pairs:
        if "=" not in pair:
            raise ParseError(f"Invalid metadata format: '{pair}' (expected key=value)")

        key, value = pair.split("=", 1)
        if key.strip() not in allowed_keys:
            raise ParseError(f"Unknown metadata key discovered: '{key}'")


def parse_info(dict_hubs):
    hubs = dict_hubs["hubs"]
    connections = dict_hubs["Connection"]
    nb_drones = dict_hubs["nb_drones"]
    valid_hub_names = {hub.name for hub in hubs}
    seen_coordinates = set()

    if nb_drones <= 0:
        raise ParseError("Number of Drones are Invalid")

    for hub in hubs:
        coords = (hub.x, hub.y)
        if coords in seen_coordinates:
            raise ParseError(f"Duplicate coordinates {coords} found "
                             f"for hub {hub.name}")
        seen_coordinates.add(coords)

    for connection in connections:
        if (connection.hub1 not in valid_hub_names or
                connection.hub2 not in valid_hub_names):
            raise ParseError("Invalid hub in Connections")

    return dict_hubs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        raw_data = extract_info(sys.argv[1])
        validated_data = parse_info(raw_data)
        print(validated_data)
    except ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
