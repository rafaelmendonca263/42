import sys
from typing import Any, Dict, Set
from structure import Connection, Hub


class ParseError(Exception):
    pass


class Parser:

    @staticmethod
    def extract_info(filepath: str) -> Dict[str, Any]:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                hubs = []
                num = 0
                connections = []

                for line in file:
                    line = line.rstrip("\r\n")
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue

                    if line.count(":") != 1:
                        raise ParseError(
                            f"Syntax Error: Invalid line format. Expected exactly one ':' separator, found {line.count(':')}: '{line.strip()}'"
                        )

                    part = line.split(":", 1)
                    command_type = part[0].strip()

                    if command_type == "nb_drones":
                        try:
                            num = int(part[1].strip())
                        except ValueError:
                            raise ParseError(
                                f"Syntax Error: Number of drones must be an integer, got '{part[1].strip()}'"
                            )
                        continue

                    elif command_type == "connection":
                        if "[" in part[1]:
                            link_data, metadata = part[1].split("[", 1)
                        else:
                            if "]" in part[1]:
                                raise ParseError(
                                    "Syntax Error: Found closing bracket ']' without opening '['."
                                )
                            link_data = part[1]
                            metadata = ""

                        clean_link = (
                            link_data.replace(" ", "")
                            .replace("\t", "")
                            .replace("\xa0", "")
                        )
                        if not clean_link:
                            raise ParseError(
                                "Syntax Error: Empty connection definition."
                            )

                        if clean_link.count("-") != 1:
                            raise ParseError(
                                f"Syntax Error: Invalid connection format (must have exactly one '-'): '{part[1].strip()}'"
                            )

                        if "]" in clean_link or "[" in clean_link:
                            raise ParseError(
                                f"Syntax Error: Unexpected tokens in connection: '{part[1].strip()}'"
                            )

                        corredores = clean_link.split("-")
                        corredor0 = corredores[0]
                        corredor1 = corredores[1]

                        if not corredor0 or not corredor1:
                            raise ParseError(
                                f"Syntax Error: Malformed connection names: '{part[1].strip()}'"
                            )

                        connections.append((Connection(corredor0, corredor1), metadata))
                        continue

                    elif command_type in ("hub", "start_hub", "end_hub"):
                        if "[" in part[1]:
                            data = part[1].split("[", 1)
                            mandatory = data[0].strip()
                            metadata = data[1]
                        else:
                            if "]" in part[1]:
                                raise ParseError(
                                    "Syntax Error: Found closing bracket ']' without opening '['."
                                )
                            mandatory = part[1].strip()
                            metadata = ""

                        coor = mandatory.split()
                        if len(coor) != 3:
                            raise ParseError(
                                f"Syntax Error: Invalid hub definition '{part[1].strip()}'. "
                                f"Expected format: 'name X Y' (exactly 3 space-separated tokens). "
                                f"Note: Hub names cannot contain spaces."
                            )

                        name = coor[0].strip()

                        # 🛑 Requisito Subject VII.4: Nomes de Hubs não podem conter hífens ('-')
                        if "-" in name:
                            raise ParseError(
                                f"Syntax Error: Hub name '{name}' cannot contain dashes ('-')."
                            )

                        try:
                            x = int(coor[1].strip())
                            y = int(coor[2].strip())
                            if not (-100000 <= x <= 100000) or not (-100000 <= y <= 100000):
                                raise ParseError(
                                    f"Syntax Error: Coordinates for hub '{name}' are out of valid range (-100000 to 100000)."
                                )
                        except ValueError:
                            raise ParseError(
                                f"Syntax Error: Coordinates for hub '{name}' must be integers, got '{coor[1]}' and '{coor[2]}'"
                            )

                        hub_type = "normal"
                        if command_type == "start_hub":
                            hub_type = "start"
                        elif command_type == "end_hub":
                            hub_type = "end"

                        hubs.append((Hub(name, x, y, hub_type, None, 1), metadata))
                        continue

                    else:
                        raise ParseError(
                            f"Syntax Error: Unknown command type discovered: '{command_type}'"
                        )

            return {"hubs": hubs, "Connection": connections, "nb_drones": num}

        except Exception as e:
            if isinstance(e, ParseError):
                raise e
            raise ParseError(f"Unexpected error while extracting information: {e}")

    @staticmethod
    def validate_metadata(metadata_str: str, allowed_keys: Set[str]) -> None:
        if metadata_str:
            if metadata_str.count("]") != 1 or "[" in metadata_str:
                raise ParseError(
                    f"Syntax Error: Invalid or unbalanced brackets in metadata: '[{metadata_str.strip()}'"
                )

            raw_check = metadata_str.strip(" \t\n\r\xa0")
            if not raw_check.endswith("]"):
                raise ParseError(
                    f"Syntax Error: Metadata must end with ']' token: '[{metadata_str.strip()}'"
                )

            content = raw_check.rstrip("]").strip(" \t\n\r\xa0")
            if not content:
                raise ParseError("Syntax Error: Metadata brackets cannot be empty")

            pairs = content.split()
            seen_local_keys = set()
            i = 0
            while i < len(pairs):
                pair = pairs[i]
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    i += 1
                else:
                    if i + 1 < len(pairs):
                        key = pair
                        value = pairs[i + 1]
                        i += 2
                    else:
                        raise ParseError("Syntax Error: Metadata key missing its value")

                clean_key = key.strip()
                if clean_key not in allowed_keys:
                    raise ParseError(
                        f"Syntax Error: Unknown metadata key discovered: '{clean_key}'"
                    )

                if clean_key in seen_local_keys:
                    raise ParseError(
                        f"Syntax Error: Duplicate metadata key '{clean_key}' discovered during syntax validation."
                    )
                seen_local_keys.add(clean_key)

    @staticmethod
    def parse_info(dict_hubs: Dict[str, Any]) -> Dict[str, Any]:
        raw_hubs = dict_hubs["hubs"]
        raw_connections = dict_hubs["Connection"]
        nb_drones = dict_hubs["nb_drones"]

        ALLOWED_HUB_KEYS = {"color", "max_drones", "zone"}
        ALLOWED_CONN_KEYS = {"max_link_capacity"}
        VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}

        if nb_drones <= 0 or nb_drones > 100000:
            raise ParseError("Business Logic Error: Number of drones must be between 1 and 100000.")

        valid_hub_names = set()
        seen_coordinates = set()
        seen_names = set()
        final_hubs = []
        start_hub_count = 0
        end_hub_count = 0

        for hub_obj, metadata in raw_hubs:
            hub_obj.zone_type = getattr(hub_obj, "zone_type", None)
            hub_obj.color = getattr(hub_obj, "color", None)
            hub_obj.max_drones = getattr(hub_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_HUB_KEYS)

            if metadata:
                content = metadata.strip(" \t\n\r\xa0").rstrip("]")
                pairs = content.split()
                seen_metadata_keys = set()
                i = 0
                while i < len(pairs):
                    pair = pairs[i]
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        i += 1
                    elif i + 1 < len(pairs):
                        k, v = pairs[i], pairs[i + 1]
                        i += 2
                    else:
                        raise ParseError("Syntax Error: Metadata key missing its value")

                    chave_limpa = k.strip()

                    if chave_limpa in seen_metadata_keys:
                        raise ParseError(f"Syntax Error: Duplicate metadata key '{chave_limpa}' found in hub definition.")
                    seen_metadata_keys.add(chave_limpa)

                    if chave_limpa == "max_drones":
                        try:
                            valor_num = int(v.strip())
                            if valor_num <= 0 or valor_num > 100000:
                                raise ParseError(f"Business Logic Error: Invalid integer value for key '{chave_limpa}': '{v.strip()}'")
                            hub_obj.max_drones = valor_num
                        except ValueError:
                            raise ParseError(f"Business Logic Error: Invalid integer value for key '{chave_limpa}': '{v.strip()}'")
                    elif chave_limpa == "zone":
                        zone_val = v.strip().lower()
                        # 🛑 Requisito Subject VII.4: Validar se o tipo de zona é um dos 4 permitidos
                        if zone_val not in VALID_ZONE_TYPES:
                            raise ParseError(
                                f"Syntax Error: Invalid zone type '{v.strip()}'. "
                                f"Must be one of: {', '.join(sorted(VALID_ZONE_TYPES))}."
                            )
                        hub_obj.zone_type = zone_val
                    elif chave_limpa == "color":
                        hub_obj.color = v.strip()

            if hub_obj.hub_type == "start":
                start_hub_count += 1
            elif hub_obj.hub_type == "end":
                end_hub_count += 1

            if hub_obj.name in seen_names:
                raise ParseError(
                    f"Business Logic Error: Duplicate hub name '{hub_obj.name}' found."
                )
            seen_names.add(hub_obj.name)

            coords = (hub_obj.x, hub_obj.y)
            if coords in seen_coordinates:
                raise ParseError(
                    f"Business Logic Error: Duplicate coordinates {coords} found for hub '{hub_obj.name}'."
                )

            seen_coordinates.add(coords)
            valid_hub_names.add(hub_obj.name)
            final_hubs.append(hub_obj)

        if start_hub_count != 1:
            raise ParseError(
                f"Business Logic Error: Map must contain exactly one 'start_hub' (found {start_hub_count})"
            )
        if end_hub_count != 1:
            raise ParseError(
                f"Business Logic Error: Map must contain exactly one 'end_hub' (found {end_hub_count})"
            )

        final_connections = []
        seen_connections = set()

        for conn_obj, metadata in raw_connections:
            conn_obj.max_drones = getattr(conn_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_CONN_KEYS)

            if metadata:
                content = metadata.strip(" \t\n\r\xa0").rstrip("]")
                pairs = content.split()
                seen_metadata_keys = set()
                i = 0
                while i < len(pairs):
                    pair = pairs[i]
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        i += 1
                    elif i + 1 < len(pairs):
                        k, v = pairs[i], pairs[i + 1]
                        i += 2
                    else:
                        raise ParseError("Syntax Error: Metadata key missing its value")

                    chave_limpa = k.strip()

                    if chave_limpa in seen_metadata_keys:
                        raise ParseError(f"Syntax Error: Duplicate metadata key '{chave_limpa}' found in connection definition.")
                    seen_metadata_keys.add(chave_limpa)

                    if chave_limpa == "max_link_capacity":
                        try:
                            valor_num = int(v.strip())
                            if valor_num <= 0 or valor_num > 100000:
                                raise ParseError(f"Business Logic Error: Invalid capacity value for connection key '{chave_limpa}': '{v.strip()}'.")
                            conn_obj.max_drones = valor_num
                        except ValueError:
                            raise ParseError(f"Business Logic Error: Invalid capacity value for connection key '{chave_limpa}': '{v.strip()}'.")

            if (
                conn_obj.from_hub not in valid_hub_names
                or conn_obj.to_hub not in valid_hub_names
            ):
                raise ParseError(
                    f"Business Logic Error: Invalid hub in Connections: {conn_obj.from_hub} -> {conn_obj.to_hub}"
                )

            if conn_obj.from_hub == conn_obj.to_hub:
                raise ParseError(
                    f"Syntax Error: Self-loop detected. Hub '{conn_obj.from_hub}' cannot connect to itself."
                )

            conn_pair = frozenset([conn_obj.from_hub, conn_obj.to_hub])
            if conn_pair in seen_connections:
                raise ParseError(
                    f"Business Logic Error: Duplicate connection detected: {conn_obj.from_hub} <-> {conn_obj.to_hub}"
                )

            seen_connections.add(conn_pair)
            final_connections.append(conn_obj)

        start_hub_name = next(h.name for h in final_hubs if h.hub_type == "start")
        end_hub_name = next(h.name for h in final_hubs if h.hub_type == "end")

        return {
            "hubs": final_hubs,
            "connections": final_connections,
            "nb_drones": nb_drones,
            "start_hub": start_hub_name,
            "end_hub": end_hub_name,
        }


def parse_map_file(filepath: str) -> Dict[str, Any]:
    raw_data = Parser.extract_info(filepath)
    return Parser.parse_info(raw_data)


parse_config = parse_map_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        validated_data = parse_map_file(sys.argv[1])
        print("=== PARSING AND VALIDATION COMPLETED SUCCESSFULLY ===")
        print(validated_data)
    except ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)