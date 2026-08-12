import re
from typing import Any, Dict, List, Set, Tuple
from structure import Connection, Hub


class ParseError(Exception):
    """Custom exception raised for syntax or logic errors during parsing."""

    pass


# Official base color mapping for visual rendering
COLOR_MAP: Dict[str, Tuple[int, int, int]] = {
    "green": (46, 204, 113),  # Start
    "red": (231, 76, 60),  # End / Danger
    "blue": (52, 152, 219),  # Normal
    "purple": (155, 89, 182),  # Maze traps
    "orange": (230, 126, 34),  # Micro gates
    "maroon": (128, 0, 0),  # Overflow
    "brown": (139, 69, 19),  # Restricted loops
    "gold": (241, 196, 15),  # Priority / False hope
    "darkred": (139, 0, 0),  # Convergence
    "violet": (142, 68, 173),  # Merge
    "crimson": (220, 20, 60),  # Torture gauntlet
    "black": (40, 40, 40),  # Dead ends / Blocked
    "cyan": (26, 188, 156),  # Final stretch
    "yellow": (255, 255, 0),  # Ok
    "lime": (0, 255, 0),  # Ok
    "magenta": (255, 0, 255),  # Ok
    "gray": (128, 128, 128),  # Gray
    "grey": (128, 128, 128),  # Grey
}


class Parser:
    """Class responsible for reading, validating, and structuring map data."""

    @staticmethod
    def extract_info(filepath: str) -> Dict[str, Any]:
        """Reads the input map file and extracts raw hub and
        connection definitions.

        Args:
            filepath (str): Path to the map file.

        Returns:
            Dict[str, Any]: Dictionary containing lists of hubs, connections,
            and extracted drone count.
        """

        line_idx = 0
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                hubs: List[Tuple[Hub, str, int]] = []
                num = 0
                connections: List[Tuple[Connection, str, int]] = []
                nb_drones_found = False
                has_instructions = False

                for raw_line in file:
                    line_idx += 1
                    line = raw_line.rstrip("\r\n")
                    if "#" in line:
                        line = line.split("#", 1)[0]
                    line = line.strip()
                    if not line:
                        continue

                    if ":" not in line:
                        raise ParseError(
                            f"[{line_idx}] Syntax Error: Invalid line format. "
                            "Missing ':' command separator"
                        )

                    part = line.split(":", 1)
                    command_type = part[0].strip()

                    if not has_instructions:
                        if command_type != "nb_drones":
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: The "
                                "first directive in the map file must be "
                                f"'nb_drones', got '{command_type}'"
                            )
                        has_instructions = True

                    if command_type == "nb_drones":
                        if nb_drones_found:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: "
                                "Duplicate 'nb_drones' directive found"
                            )
                        try:
                            num = int(part[1].strip())
                        except ValueError:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: Number of "
                                "drones must be an integer, "
                                f"got '{part[1].strip()}'"
                            )
                        nb_drones_found = True
                        continue

                    elif command_type == "connection":
                        if "[" in part[1]:
                            link_data, metadata = part[1].split("[", 1)
                        else:
                            if "]" in part[1]:
                                raise ParseError(
                                    f"[{line_idx}] Syntax Error: "
                                    "Found closing bracket ']' without "
                                    "opening '['"
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
                                f"[{line_idx}] Syntax Error: "
                                "Empty connection definition"
                            )

                        if clean_link.count("-") != 1:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: "
                                "Invalid connection format "
                                "(must have exactly one '-'): "
                                f"'{part[1].strip()}'"
                            )

                        if "]" in clean_link or "[" in clean_link:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: "
                                "Unexpected tokens in connection: "
                                f"'{part[1].strip()}'"
                            )

                        corridors = clean_link.split("-")
                        corridor0 = corridors[0]
                        corridor1 = corridors[1]

                        if not corridor0 or not corridor1:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: "
                                "Malformed connection names: "
                                f"'{part[1].strip()}'"
                            )

                        connections.append(
                            (
                                Connection(corridor0, corridor1),
                                metadata,
                                line_idx,
                            )
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
                                    f"[{line_idx}] Syntax Error: "
                                    "Found closing bracket ']' "
                                    "without opening '['"
                                )
                            mandatory = part[1].strip()
                            metadata = ""

                        coor = mandatory.split()
                        if len(coor) != 3:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: "
                                f"Invalid hub definition '{part[1].strip()}'. "
                                "Expected format: 'name X Y'"
                            )

                        name = coor[0].strip()

                        if "-" in name:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: Hub name "
                                f"'{name}' "
                                "cannot contain dashes ('-')"
                            )

                        try:
                            x = int(coor[1].strip())
                            y = int(coor[2].strip())
                        except ValueError:
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: Coordinates "
                                f"for hub '{name}' must be integers, "
                                f"got '{coor[1]}' and '{coor[2]}'"
                            )

                        if not (-100000 <= x <= 100000) or not (
                            -100000 <= y <= 100000
                        ):
                            raise ParseError(
                                f"[{line_idx}] Syntax Error: Coordinates "
                                f"for hub '{name}' are out of valid range "
                                "(-100000 to 100000)"
                            )

                        hub_type = "normal"
                        if command_type == "start_hub":
                            hub_type = "start"
                        elif command_type == "end_hub":
                            hub_type = "end"

                        hubs.append(
                            (
                                Hub(name, x, y, hub_type, None, 1),
                                metadata,
                                line_idx,
                            )
                        )
                        continue

                    else:
                        raise ParseError(
                            f"[{line_idx}] Syntax Error: Unknown "
                            f"command type discovered: '{command_type}'"
                        )

            if not nb_drones_found:
                raise ParseError(
                    f"[{line_idx}] Syntax Error: Missing "
                    "'nb_drones' directive in map file"
                )

            return {"hubs": hubs, "connections": connections, "nb_drones": num}

        except Exception as e:
            if isinstance(e, ParseError):
                raise e
            raise ParseError(
                f"[{line_idx}] Unexpected error while extracting "
                f"information: {e}"
            )

    @staticmethod
    def validate_metadata(
        metadata_str: str, allowed_keys: Set[str], line_num: int = 0
    ) -> None:
        """Validates the syntax and keys of a metadata block.

        Args:
            metadata_str (str): String containing the metadata.
            allowed_keys (Set[str]): Set of allowed keys.
            line_num (int): Corresponding line number in the file.
        """

        prefix = f"[{line_num}] " if line_num > 0 else ""
        if metadata_str is not None and metadata_str != "":
            if metadata_str.count("]") != 1 or "[" in metadata_str:
                raise ParseError(
                    f"{prefix}Syntax Error: Invalid or unbalanced "
                    f"brackets in metadata: '[{metadata_str.strip()}'"
                )

            raw_check = metadata_str.strip(" \t\n\r\xa0")
            if not raw_check.endswith("]"):
                raise ParseError(
                    f"{prefix}Syntax Error: Metadata must end with ']'"
                    f" token: '[{metadata_str.strip()}'"
                )

            content = raw_check.rstrip("]").strip(" \t\n\r\xa0")
            if not content:
                raise ParseError(
                    f"{prefix}Syntax Error: Metadata brackets cannot be empty"
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
                            f"{prefix}Syntax Error: Invalid key-value "
                            f"format in metadata '{pair}'. Expected single "
                            "'=' separator."
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
                            f"{prefix}Syntax Error: Metadata key '{pair}' "
                            "missing its value."
                        )

                clean_key = key.strip()
                clean_val = value.strip()

                if not clean_key or not clean_val:
                    raise ParseError(
                        f"{prefix}Syntax Error: Empty key or value in "
                        "metadata expression."
                    )

                if clean_key not in allowed_keys:
                    raise ParseError(
                        f"{prefix}Syntax Error: Unknown metadata "
                        f"key discovered: '{clean_key}'"
                    )

                if clean_key in seen_local_keys:
                    raise ParseError(
                        f"{prefix}Syntax Error: Duplicate metadata "
                        f"key '{clean_key}' discovered during syntax "
                        "validation."
                    )
                seen_local_keys.add(clean_key)

    @staticmethod
    def validate_graph_reachability(
        hubs: List[Hub],
        connections: List[Connection],
        start_name: str,
        end_name: str,
        start_line: int,
        end_line: int,
    ) -> None:
        """Verifies that at least one valid path exists between start_hub
        and end_hub using BFS.

        Args:
            hubs (List[Hub]): List of hubs in the graph.
            connections (List[Connection]): List of connections in the graph.
            start_name (str): Name of the start hub.
            end_name (str): Name of the end hub.
            start_line (int): Line number of the start hub.
            end_line (int): Line number of the end hub.
        """

        adj: Dict[str, List[str]] = {
            h.name: [] for h in hubs if h.zone_type != "blocked"
        }
        for conn in connections:
            if conn.from_hub in adj and conn.to_hub in adj:
                adj[conn.from_hub].append(conn.to_hub)
                adj[conn.to_hub].append(conn.from_hub)

        if not adj.get(start_name):
            raise ParseError(
                f"[{start_line}] Logic Error: Start hub '{start_name}' has "
                "no valid connections."
            )
        if not adj.get(end_name):
            raise ParseError(
                f"[{end_line}] Logic Error: End hub '{end_name}' has "
                "no valid connections."
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
            f"[{start_line}] Logic Error: No valid path exists from "
            f"start hub '{start_name}' to end hub '{end_name}'."
        )

    @staticmethod
    def parse_info(dict_hubs: Dict[str, Any]) -> Dict[str, Any]:
        """Processes metadata, validates types/values, and enforces graph
        accessibility rules.

        Args:
            dict_hubs (Dict[str, Any]): Raw dictionary containing hubs,
            connections, and drones.

        Returns:
            Dict[str, Any]: Validated and structured map configuration.
        """

        raw_hubs = dict_hubs["hubs"]
        raw_connections = dict_hubs["connections"]
        nb_drones = dict_hubs["nb_drones"]

        ALLOWED_HUB_KEYS = {"color", "max_drones", "zone"}
        ALLOWED_CONN_KEYS = {"max_link_capacity"}
        VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}

        if nb_drones <= 0 or nb_drones > 100000:
            raise ParseError(
                "[1] Logic Error: Number of drones must "
                "be between 1 and 100000."
            )

        valid_hub_names = set()
        seen_coordinates = set()
        seen_names = set()
        final_hubs = []
        start_hub_count = 0
        end_hub_count = 0
        start_line_num = 1
        end_line_num = 1

        for hub_obj, metadata, line_num in raw_hubs:
            hub_obj.zone_type = getattr(hub_obj, "zone_type", "normal")
            hub_obj.color = getattr(hub_obj, "color", None)
            hub_obj.max_drones = getattr(hub_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_HUB_KEYS, line_num)

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
                            f"[{line_num}] Syntax Error: Metadata key "
                            "missing its value"
                        )

                    clean_key = k.strip()
                    clean_val = v.strip()

                    if not clean_val:
                        raise ParseError(
                            f"[{line_num}] Syntax Error: Metadata "
                            f"key '{clean_key}' has an empty value."
                        )

                    if clean_key in seen_metadata_keys:
                        raise ParseError(
                            f"[{line_num}] Syntax Error: Duplicate "
                            f"metadata key '{clean_key}' found in "
                            "hub definition."
                        )
                    seen_metadata_keys.add(clean_key)

                    if clean_key == "max_drones":
                        try:
                            value_num = int(clean_val)
                            if value_num <= 0 or value_num > 100000:
                                raise ParseError(
                                    f"[{line_num}] Logic Error: "
                                    f"Invalid integer value for "
                                    f"key '{clean_key}': '{clean_val}'"
                                )
                            hub_obj.max_drones = value_num
                        except ValueError:
                            raise ParseError(
                                f"[{line_num}] Logic Error: "
                                f"Invalid integer value for key '{clean_key}':"
                                f" '{clean_val}'"
                            )
                    elif clean_key == "zone":
                        zone_val = clean_val.lower()
                        if zone_val not in VALID_ZONE_TYPES:
                            raise ParseError(
                                f"[{line_num}] Syntax Error: Invalid zone "
                                f"type '{clean_val}'. Must be one "
                                f"of: {', '.join(sorted(VALID_ZONE_TYPES))}."
                            )
                        hub_obj.zone_type = zone_val
                    elif clean_key == "color":
                        color_val = clean_val.lower()
                        if not re.match(r"^[a-zA-Z0-9_]+$", color_val):
                            raise ParseError(
                                f"[{line_num}] Syntax Error: Invalid "
                                f"color '{clean_val}'. Color must be "
                                "a single word string."
                            )
                        hub_obj.color = color_val

            if hub_obj.hub_type == "start":
                start_hub_count += 1
                hub_obj.max_drones = 1000000
                start_line_num = line_num
            elif hub_obj.hub_type == "end":
                end_hub_count += 1
                hub_obj.max_drones = 1000000
                end_line_num = line_num

            if hub_obj.name in seen_names:
                raise ParseError(
                    f"[{line_num}] Logic Error: Duplicate hub "
                    f"name '{hub_obj.name}' found."
                )
            seen_names.add(hub_obj.name)

            coords = (hub_obj.x, hub_obj.y)
            if coords in seen_coordinates:
                raise ParseError(
                    f"[{line_num}] Logic Error: Duplicate "
                    f"coordinates {coords} found for hub '{hub_obj.name}'."
                )

            seen_coordinates.add(coords)
            valid_hub_names.add(hub_obj.name)
            final_hubs.append(hub_obj)

        if start_hub_count != 1:
            raise ParseError(
                f"[{start_line_num}] Logic Error: Map must contain exactly "
                f"one 'start_hub' (found {start_hub_count})"
            )
        if end_hub_count != 1:
            raise ParseError(
                f"[{end_line_num}] Logic Error: Map must contain exactly one "
                f"'end_hub' (found {end_hub_count})"
            )

        final_connections = []
        seen_connections = set()

        for conn_obj, metadata, line_num in raw_connections:
            conn_obj.max_drones = getattr(conn_obj, "max_drones", 1)
            Parser.validate_metadata(metadata, ALLOWED_CONN_KEYS, line_num)

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
                            f"[{line_num}] Syntax Error: Metadata key "
                            "missing its value"
                        )

                    clean_key = k.strip()
                    clean_val = v.strip()

                    if not clean_val:
                        raise ParseError(
                            f"[{line_num}] Syntax Error: Metadata "
                            f"key '{clean_key}' has an empty value."
                        )

                    if clean_key in seen_metadata_keys:
                        raise ParseError(
                            f"[{line_num}] Syntax Error: Duplicate "
                            f"metadata key '{clean_key}' found in "
                            "connection definition."
                        )
                    seen_metadata_keys.add(clean_key)

                    if clean_key == "max_link_capacity":
                        try:
                            value_num = int(clean_val)
                            if value_num <= 0 or value_num > 100000:
                                raise ParseError(
                                    f"[{line_num}] Logic Error: "
                                    f"Invalid capacity value "
                                    f"for connection key '{clean_key}':"
                                    f" '{clean_val}'."
                                )
                            conn_obj.max_drones = value_num
                        except ValueError:
                            raise ParseError(
                                f"[{line_num}] Logic Error: "
                                "Invalid capacity value for connection "
                                f"key '{clean_key}': '{clean_val}'."
                            )

            if (
                conn_obj.from_hub not in valid_hub_names
                or conn_obj.to_hub not in valid_hub_names
            ):
                raise ParseError(
                    f"[{line_num}] Logic Error: Invalid hub "
                    f"in Connections: {conn_obj.from_hub} -> {conn_obj.to_hub}"
                )

            if conn_obj.from_hub == conn_obj.to_hub:
                raise ParseError(
                    f"[{line_num}] Syntax Error: Self-loop detected. "
                    f"Hub '{conn_obj.from_hub}' cannot connect to itself."
                )

            conn_pair = frozenset([conn_obj.from_hub, conn_obj.to_hub])
            if conn_pair in seen_connections:
                raise ParseError(
                    f"[{line_num}] Logic Error: Duplicate "
                    f"connection detected: {conn_obj.from_hub} <-> "
                    f"{conn_obj.to_hub}"
                )

            seen_connections.add(conn_pair)
            final_connections.append(conn_obj)

        start_hub_name = next(
            h.name for h in final_hubs if h.hub_type == "start"
        )
        end_hub_name = next(h.name for h in final_hubs if h.hub_type == "end")

        Parser.validate_graph_reachability(
            final_hubs,
            final_connections,
            start_hub_name,
            end_hub_name,
            start_line_num,
            end_line_num,
        )

        return {
            "hubs": final_hubs,
            "connections": final_connections,
            "nb_drones": nb_drones,
            "start_hub": start_hub_name,
            "end_hub": end_hub_name,
        }


def parse_map_file(filepath: str) -> Dict[str, Any]:
    """Main entry point function for map file parsing.

    Args:
        filepath (str): Path to the map file.

    Returns:
        Dict[str, Any]: Complete and validated map configuration.
    """

    raw_data = Parser.extract_info(filepath)
    return Parser.parse_info(raw_data)


parse_config = parse_map_file
