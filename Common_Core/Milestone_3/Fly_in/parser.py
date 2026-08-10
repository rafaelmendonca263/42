"""Module responsible for parsing and validating map files for Fly-in."""

import re
from typing import Any, Dict, List, Set, Tuple
from structure import Connection, Hub


class ParseError(Exception):
    """Custom exception raised for syntax or
    business logic errors during parsing."""

    pass


# Official color mapping for visual rendering
COLOR_MAP: Dict[str, Tuple[int, int, int]] = {
    "green": (46, 204, 113),   # Start
    "red": (231, 76, 60),      # End / Danger
    "blue": (52, 152, 219),    # Normal
    "purple": (155, 89, 182),  # Maze traps
    "orange": (230, 126, 34),  # Micro gates
    "maroon": (128, 0, 0),     # Overflow
    "brown": (139, 69, 19),    # Restricted loops
    "gold": (241, 196, 15),    # Priority / False hope
    "darkred": (139, 0, 0),    # Convergence
    "violet": (142, 68, 173),  # Merge
    "crimson": (220, 20, 60),  # Torture gauntlet
    "black": (40, 40, 40),     # Dead ends / Blocked
    "cyan": (26, 188, 156),    # Final stretch
    "yellow": (255, 255, 0),   # Ok
    "lime": (0, 255, 0),       # Ok
    "magenta": (255, 0, 255),  # Ok
    "rainbow": (0, 0, 0)       # Rainbow
}

VALID_COLORS: Set[str] = set(COLOR_MAP.keys())


class Parser:
    """Class responsible for reading, validating, and structuring map data."""

    @staticmethod
    def extract_info(filepath: str) -> Dict[str, Any]:
        """Reads the input map file and extracts raw
        hub and connection definitions."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                hubs: List[Tuple[Hub, str]] = []
                num = 0
                connections: List[Tuple[Connection, str]] = []
                nb_drones_found = False
                has_instructions = False

                for line in file:
                    line = line.rstrip("\r\n")
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue

                    if ":" not in line:
                        raise ParseError(
                            "Syntax Error: Invalid line format. "
                            f"Missing ':' command separator in line: '{line}'"
                        )

                    part = line.split(":", 1)
                    command_type = part[0].strip()

                    if not has_instructions:
                        if command_type != "nb_drones":
                            raise ParseError(
                                "Syntax Error: The first "
                                "directive in the map file "
                                f"must be 'nb_drones', got '{command_type}'."
                            )
                        has_instructions = True

                    if command_type == "nb_drones":
                        if nb_drones_found:
                            raise ParseError(
                                "Syntax Error: Duplicate 'nb_drones' "
                                "directive found."
                            )
                        try:
                            num = int(part[1].strip())
                        except ValueError:
                            raise ParseError(
                                "Syntax Error: Number of drones must be "
                                f"an integer, got '{part[1].strip()}'"
                            )
                        nb_drones_found = True
                        continue

                    elif command_type == "connection":
                        if "[" in part[1]:
                            link_data, metadata = part[1].split("[", 1)
                        else:
                            if "]" in part[1]:
                                raise ParseError(
                                    "Syntax Error: Found closing bracket ']'"
                                    " without opening '['."
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
                                "Syntax Error: Invalid connection format "
                                "(must have exactly one '-'): "
                                f"'{part[1].strip()}'"
                            )

                        if "]" in clean_link or "[" in clean_link:
                            raise ParseError(
                                "Syntax Error: Unexpected tokens "
                                "in connection: "
                                f"'{part[1].strip()}'"
                            )

                        corridors = clean_link.split("-")
                        corridor0 = corridors[0]
                        corridor1 = corridors[1]

                        if not corridor0 or not corridor1:
                            raise ParseError(
                                "Syntax Error: Malformed connection names: "
                                f"'{part[1].strip()}'"
                            )

                        connections.append(
                            (Connection(corridor0, corridor1), metadata)
                        )
                        continue

                    elif command_type in ("hub", "start_hub", "end_hub"):
                        if "[" in part[1]:
                            data = part[1].split("[", 1)
                            mandatory = data[0].strip()
                            metadata = data[1]
                        else:
                            if "]" in part[1]:
                                raise ParseError(
                                    "Syntax Error: Found closing bracket ']' "
                                    "without opening '['."
                                )
                            mandatory = part[1].strip()
                            metadata = ""

                        coor = mandatory.split()
                        if len(coor) != 3:
                            raise ParseError(
                                "Syntax Error: Invalid hub definition "
                                f"'{part[1].strip()}'. Expected format: "
                                "'name X Y' (exactly 3 "
                                "space-separated tokens)."
                            )

                        name = coor[0].strip()

                        # Subject rule: Hub names cannot contain dashes ('-')
                        # as it's reserved for connections. Colons (':') and
                        # other chars are allowed.
                        if "-" in name:
                            raise ParseError(
                                "Syntax Error: Hub name "
                                f"'{name}' cannot contain dashes ('-')."
                            )

                        try:
                            x = int(coor[1].strip())
                            y = int(coor[2].strip())
                        except ValueError:
                            raise ParseError(
                                "Syntax Error: Coordinates for hub "
                                f"'{name}' must be integers, got '{coor[1]}'"
                                f" and '{coor[2]}'"
                            )

                        if not (-100000 <= x <= 100000) or not (
                            -100000 <= y <= 100000
                        ):
                            raise ParseError(
                                "Syntax Error: Coordinates for hub "
                                f"'{name}' are out of valid range "
                                "(-100000 to 100000)."
                            )

                        hub_type = "normal"
                        if command_type == "start_hub":
                            hub_type = "start"
                        elif command_type == "end_hub":
                            hub_type = "end"

                        hubs.append(
                            (Hub(name, x, y, hub_type, None, 1), metadata)
                        )
                        continue

                    else:
                        raise ParseError(
                            "Syntax Error: Unknown command type discovered: "
                            f"'{command_type}'"
                        )

            if not nb_drones_found:
                raise ParseError(
                    "Syntax Error: Missing 'nb_drones' directive in map file."
                )

            return {"hubs": hubs, "connections": connections, "nb_drones": num}

        except Exception as e:
            if isinstance(e, ParseError):
                raise e
            raise ParseError(
                f"Unexpected error while extracting information: {e}"
            )

    @staticmethod
    def validate_metadata(metadata_str: str, allowed_keys: Set[str]) -> None:
        """Validates the syntax and keys of a metadata block,
        accepting arbitrary spacing."""
        if metadata_str:
            if metadata_str.count("]") != 1 or "[" in metadata_str:
                raise ParseError(
                    "Syntax Error: Invalid or unbalanced brackets in "
                    f"metadata: '[{metadata_str.strip()}'"
                )

            raw_check = metadata_str.strip(" \t\n\r\xa0")
            if not raw_check.endswith("]"):
                raise ParseError(
                    "Syntax Error: Metadata must end with ']' "
                    f"token: '[{metadata_str.strip()}'"
                )

            content = raw_check.rstrip("]").strip(" \t\n\r\xa0")
            if not content:
                raise ParseError(
                    "Syntax Error: Metadata brackets cannot be empty"
                )

            content_clean = content.replace("\xa0", " ").replace("\t", " ")
            content_normalized = re.sub(r"\s*=\s*", "=", content_clean)

            pairs = content_normalized.split()
            seen_local_keys: Set[str] = set()
            i = 0

            while i < len(pairs):
                pair = pairs[i]

                if "=" in pair:
                    if pair.count("=") != 1:
                        raise ParseError(
                            "Syntax Error: Invalid key-value "
                            "format in metadata "
                            f"'{pair}'. Expected single '=' separator."
                        )
                    key, value = pair.split("=", 1)
                    i += 1
                else:
                    if i + 1 < len(pairs) and "=" not in pairs[i + 1]:
                        key = pair
                        value = pairs[i + 1]
                        i += 2
                    else:
                        raise ParseError(
                            f"Syntax Error: Metadata key '{pair}' missing "
                            "its value."
                        )

                clean_key = key.strip()
                clean_val = value.strip()

                if not clean_key or not clean_val:
                    raise ParseError(
                        "Syntax Error: Empty key or value in "
                        "metadata expression."
                    )

                if clean_key not in allowed_keys:
                    raise ParseError(
                        "Syntax Error: Unknown metadata key discovered: "
                        f"'{clean_key}'"
                    )

                if clean_key in seen_local_keys:
                    raise ParseError(
                        f"Syntax Error: Duplicate metadata key '{clean_key}' "
                        "discovered during syntax validation."
                    )
                seen_local_keys.add(clean_key)

    @staticmethod
    def validate_graph_reachability(
        hubs: List[Hub],
        connections: List[Connection],
        start_name: str,
        end_name: str,
    ) -> None:
        """Verifies that at least one valid path exists between
        start_hub and end_hub using BFS."""
        adj: Dict[str, List[str]] = {h.name: [] for h in hubs}
        for conn in connections:
            adj[conn.from_hub].append(conn.to_hub)
            adj[conn.to_hub].append(conn.from_hub)

        if not adj[start_name]:
            raise ParseError(
                f"Business Logic Error: Start hub '{start_name}' "
                "has no connections."
            )
        if not adj[end_name]:
            raise ParseError(
                f"Business Logic Error: End hub '{end_name}'"
                " has no connections."
            )

        visited = set([start_name])
        queue = [start_name]

        while queue:
            current = queue.pop(0)
            if current == end_name:
                return

            for neighbor in adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        raise ParseError(
            "Business Logic Error: No valid path exists from start hub "
            f"'{start_name}' to end hub '{end_name}'."
        )

    @staticmethod
    def parse_info(dict_hubs: Dict[str, Any]) -> Dict[str, Any]:
        """Processes metadata, validates types/values, and enforces
        graph reachability rules."""
        raw_hubs = dict_hubs["hubs"]
        raw_connections = dict_hubs["connections"]
        nb_drones = dict_hubs["nb_drones"]

        ALLOWED_HUB_KEYS = {"color", "max_drones", "zone"}
        ALLOWED_CONN_KEYS = {"max_link_capacity"}
        VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}

        if nb_drones <= 0 or nb_drones > 100000:
            raise ParseError(
                "Business Logic Error: Number of drones must be "
                "between 1 and 100000."
            )

        valid_hub_names = set()
        seen_coordinates = set()
        seen_names = set()
        final_hubs = []
        start_hub_count = 0
        end_hub_count = 0

        for hub_obj, metadata in raw_hubs:
            hub_obj.zone_type = getattr(hub_obj, "zone_type", "normal")
            hub_obj.color = getattr(hub_obj, "color", None)
            hub_obj.max_drones = getattr(hub_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_HUB_KEYS)

            if metadata:
                content = metadata.strip(" \t\n\r\xa0").rstrip("]")
                content_clean = content.replace("\xa0", " ").replace("\t", " ")
                content_normalized = re.sub(r"\s*=\s*", "=", content_clean)
                pairs = content_normalized.split()

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
                        raise ParseError(
                            "Syntax Error: Metadata key missing its value"
                        )

                    clean_key = k.strip()
                    clean_val = v.strip()

                    if not clean_val:
                        raise ParseError(
                            f"Syntax Error: Metadata key '{clean_key}' has "
                            "an empty value."
                        )

                    if clean_key in seen_metadata_keys:
                        raise ParseError(
                            "Syntax Error: Duplicate metadata "
                            f"key '{clean_key}' found in hub definition."
                        )
                    seen_metadata_keys.add(clean_key)

                    if clean_key == "max_drones":
                        try:
                            value_num = int(clean_val)
                            if value_num <= 0 or value_num > 100000:
                                raise ParseError(
                                    "Business Logic Error: Invalid integer "
                                    "value for key "
                                    f"'{clean_key}': '{clean_val}'"
                                )
                            hub_obj.max_drones = value_num
                        except ValueError:
                            raise ParseError(
                                "Business Logic Error: Invalid integer "
                                f"value for key '{clean_key}': '{clean_val}'"
                            )
                    elif clean_key == "zone":
                        zone_val = clean_val.lower()
                        if zone_val not in VALID_ZONE_TYPES:
                            raise ParseError(
                                "Syntax Error: Invalid zone "
                                f"type '{clean_val}'. "
                                "Must be one of: "
                                f"{', '.join(sorted(VALID_ZONE_TYPES))}."
                            )
                        hub_obj.zone_type = zone_val
                    elif clean_key == "color":
                        color_val = clean_val.lower()
                        if color_val not in VALID_COLORS:
                            raise ParseError(
                                f"Syntax Error: Invalid color '{clean_val}'. "
                                "Must be one of: "
                                f"{', '.join(sorted(VALID_COLORS))}."
                            )
                        hub_obj.color = color_val

            if hub_obj.hub_type == "start":
                start_hub_count += 1
            elif hub_obj.hub_type == "end":
                end_hub_count += 1

            if hub_obj.name in seen_names:
                raise ParseError(
                    "Business Logic Error: Duplicate "
                    f"hub name '{hub_obj.name}' found."
                )
            seen_names.add(hub_obj.name)

            coords = (hub_obj.x, hub_obj.y)
            if coords in seen_coordinates:
                raise ParseError(
                    "Business Logic Error: Duplicate coordinates "
                    f"{coords} found for hub '{hub_obj.name}'."
                )

            seen_coordinates.add(coords)
            valid_hub_names.add(hub_obj.name)
            final_hubs.append(hub_obj)

        if start_hub_count != 1:
            raise ParseError(
                "Business Logic Error: Map must contain exactly "
                f"one 'start_hub' (found {start_hub_count})"
            )
        if end_hub_count != 1:
            raise ParseError(
                "Business Logic Error: Map must contain exactly one "
                f"'end_hub' (found {end_hub_count})"
            )

        final_connections = []
        seen_connections = set()

        for conn_obj, metadata in raw_connections:
            conn_obj.max_drones = getattr(conn_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_CONN_KEYS)

            if metadata:
                content = metadata.strip(" \t\n\r\xa0").rstrip("]")
                content_clean = content.replace("\xa0", " ").replace("\t", " ")
                content_normalized = re.sub(r"\s*=\s*", "=", content_clean)
                pairs = content_normalized.split()

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
                        raise ParseError(
                            "Syntax Error: Metadata key missing its value"
                        )

                    clean_key = k.strip()
                    clean_val = v.strip()

                    if not clean_val:
                        raise ParseError(
                            f"Syntax Error: Metadata key '{clean_key}' has "
                            "an empty value."
                        )

                    if clean_key in seen_metadata_keys:
                        raise ParseError(
                            "Syntax Error: Duplicate metadata key "
                            f"'{clean_key}' found in connection definition."
                        )
                    seen_metadata_keys.add(clean_key)

                    if clean_key == "max_link_capacity":
                        try:
                            value_num = int(clean_val)
                            if value_num <= 0 or value_num > 100000:
                                raise ParseError(
                                    "Business Logic Error: Invalid "
                                    "capacity value for connection "
                                    f"key '{clean_key}': '{clean_val}'."
                                )
                            conn_obj.max_drones = value_num
                        except ValueError:
                            raise ParseError(
                                "Business Logic Error: Invalid capacity "
                                "value for connection "
                                f"key '{clean_key}': '{clean_val}'."
                            )

            if (
                conn_obj.from_hub not in valid_hub_names
                or conn_obj.to_hub not in valid_hub_names
            ):
                raise ParseError(
                    "Business Logic Error: Invalid hub in "
                    f"Connections: {conn_obj.from_hub} -> {conn_obj.to_hub}"
                )

            if conn_obj.from_hub == conn_obj.to_hub:
                raise ParseError(
                    "Syntax Error: Self-loop detected. "
                    f"Hub '{conn_obj.from_hub}' cannot connect to itself."
                )

            conn_pair = frozenset([conn_obj.from_hub, conn_obj.to_hub])
            if conn_pair in seen_connections:
                raise ParseError(
                    "Business Logic Error: Duplicate connection "
                    f"detected: {conn_obj.from_hub} <-> {conn_obj.to_hub}"
                )

            seen_connections.add(conn_pair)
            final_connections.append(conn_obj)

        start_hub_name = next(
            h.name for h in final_hubs if h.hub_type == "start"
        )
        end_hub_name = next(h.name for h in final_hubs if h.hub_type == "end")

        Parser.validate_graph_reachability(
            final_hubs, final_connections, start_hub_name, end_hub_name
        )

        return {
            "hubs": final_hubs,
            "connections": final_connections,
            "nb_drones": nb_drones,
            "start_hub": start_hub_name,
            "end_hub": end_hub_name,
        }


def parse_map_file(filepath: str) -> Dict[str, Any]:
    """Main entry point function for map file parsing."""
    raw_data = Parser.extract_info(filepath)
    return Parser.parse_info(raw_data)


parse_config = parse_map_file
