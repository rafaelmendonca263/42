import sys
from structure import Hub, Connection


class ParseError(Exception):
    pass


class Parser:

    @staticmethod
    def extract_info(filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                hubs = []
                num = 0
                connections = []

                for line in file:
                    line = line.rstrip('\r\n')
                    if '#' in line:
                        line = line.split('#', 1)[0]
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.count(":") != 1:
                        raise ParseError(f"Syntax Error: Invalid line format. Expected exactly one ':' separator, found {line.count(':')}: '{line.strip()}'")

                    part = line.split(":", 1)
                    type = part[0].strip()

                    if type == "nb_drones":
                        try:
                            num = int(part[1].strip())
                        except ValueError:
                            raise ParseError(f"Syntax Error: Number of drones must be an integer, got '{part[1].strip()}'")
                        continue
                    
                    elif type == "connection":
                        if "[" in part[1]:
                            link_data, metadata = part[1].split("[", 1)
                        else:
                            if "]" in part[1]:
                                raise ParseError("Syntax Error: Found closing bracket ']' without opening '['.")
                            link_data = part[1]
                            metadata = ""

                        clean_link = link_data.replace(" ", "").replace("\t", "").replace("\xa0", "")
                        if not clean_link:
                            raise ParseError(f"Syntax Error: Empty connection definition.")

                        if clean_link.count("-") != 1:
                            raise ParseError(f"Syntax Error: Invalid connection format (must have exactly one '-'): '{part[1].strip()}'")

                        if "]" in clean_link or "[" in clean_link:
                            raise ParseError(f"Syntax Error: Unexpected tokens in connection: '{part[1].strip()}'")

                        corredores = clean_link.split("-")
                        corredor0 = corredores[0]
                        corredor1 = corredores[1]

                        if not corredor0 or not corredor1:
                            raise ParseError(f"Syntax Error: Malformed connection names: '{part[1].strip()}'")

                        connections.append((Connection(corredor0, corredor1), metadata))
                        continue
                    
                    elif type in ("hub", "start_hub", "end_hub"):
                        if "[" in part[1]:
                            data = part[1].split("[", 1)
                            mandatory = data[0].strip()
                            metadata = data[1]
                            coor = mandatory.split()
                        else:
                            if "]" in part[1]:
                                raise ParseError("Syntax Error: Found closing bracket ']' without opening '['.")
                            data = part[1]
                            coor = data.split()
                            metadata = ""

                        if len(coor) != 3:
                            raise ParseError(f"Syntax Error: Invalid number of parameters for hub definition: '{part[1].strip()}'")

                        name = coor[0].strip()
                        try:
                            x = int(coor[1].strip())
                            y = int(coor[2].strip())
                        except ValueError:
                            raise ParseError(f"Syntax Error: Coordinates for hub '{name}' must be integers, got '{coor[1]}' and '{coor[2]}'")

                        hub_type = "normal"
                        if type == "start_hub":
                            hub_type = "start"
                        elif type == "end_hub":
                            hub_type = "end"

                        hubs.append((Hub(name, x, y, hub_type, None, 1), metadata))
                        continue

                    else:
                        raise ParseError(f"Syntax Error: Unknown command type discovered: '{type}'")

            return {
                "hubs": hubs,
                "Connection": connections,
                "nb_drones": num
            }

        except Exception as e:
            if isinstance(e, ParseError):
                raise e
            raise ParseError(f"Not expected error while extracting information: {e}")

    @staticmethod
    def validate_metadata(metadata_str: str, allowed_keys: set):
        if metadata_str:
            if metadata_str.count(']') != 1 or '[' in metadata_str:
                raise ParseError(f"Syntax Error: Invalid or unbalanced brackets in metadata: '[{metadata_str.strip()}'")

            raw_check = metadata_str.strip(" \t\n\r\xa0")
            if not raw_check.endswith(']'):
                raise ParseError(f"Syntax Error: Metadata must end with ']' token: '[{metadata_str.strip()}'")

            content = raw_check.rstrip(']').strip(" \t\n\r\xa0")
            if not content:
                raise ParseError("Syntax Error: Metadata brackets cannot be empty")

            pairs = content.split()
            for pair in pairs:
                if "=" not in pair:
                    raise ParseError(f"Invalid metadata format: '{pair}' (expected key=value)")

                key, value = pair.split("=", 1)
                if key.strip() not in allowed_keys:
                   raise ParseError(f"Unknown metadata key discovered: '{key.strip()}'")

    @staticmethod
    def parse_info(dict_hubs):
        raw_hubs = dict_hubs["hubs"]
        raw_connections = dict_hubs["Connection"]
        nb_drones = dict_hubs["nb_drones"]

        ALLOWED_HUB_KEYS = {"color", "max_drones", "zone"}
        ALLOWED_CONN_KEYS = {"max_link_capacity"}

        if nb_drones <= 0:
            raise ParseError("Number of Drones are Invalid")

        valid_hub_names = set()
        seen_coordinates = set()
        final_hubs = []
        start_hub_count = 0
        end_hub_count = 0

        for hub_obj, metadata in raw_hubs:
            # Corrigido para chamar o método estático dentro da classe
            Parser.validate_metadata(metadata, ALLOWED_HUB_KEYS)

            if hub_obj.hub_type == "start":
                start_hub_count += 1
            elif hub_obj.hub_type == "end":
                end_hub_count += 1

            coords = (hub_obj.x, hub_obj.y)
            if coords in seen_coordinates:
                raise ParseError(f"Duplicate coordinates {coords} found for hub {hub_obj.name}")

            seen_coordinates.add(coords)
            valid_hub_names.add(hub_obj.name)
            final_hubs.append(hub_obj)

        if start_hub_count != 1:
            raise ParseError(f"Business Logic Error: Map must contain exactly one 'start_hub' (found {start_hub_count})")
        if end_hub_count != 1:
            raise ParseError(f"Business Logic Error: Map must contain exactly one 'end_hub' (found {end_hub_count})")

        final_connections = []
        seen_connections = set()

        for conn_obj, metadata in raw_connections:
            # Corrigido para chamar o método estático dentro da classe
            Parser.validate_metadata(metadata, ALLOWED_CONN_KEYS)

            if (conn_obj.hub1 not in valid_hub_names or
                    conn_obj.hub2 not in valid_hub_names):
                raise ParseError(f"Invalid hub in Connections: {conn_obj.hub1} -> {conn_obj.hub2}")

            if conn_obj.hub1 == conn_obj.hub2:
                raise ParseError(f"Syntax Error: Self-loop detected. Hub '{conn_obj.hub1}' cannot connect to itself.")

            conn_pair = frozenset([conn_obj.hub1, conn_obj.hub2])
            if conn_pair in seen_connections:
                raise ParseError(f"Duplicate connection detected: {conn_obj.hub1} <-> {conn_obj.hub2}")

            seen_connections.add(conn_pair)
            final_connections.append(conn_obj)

        dict_hubs["hubs"] = final_hubs
        dict_hubs["Connection"] = final_connections

        return dict_hubs


# Exemplo de como usar no teu main.py ou bloco de execução:
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        # Chamada direta usando o nome da classe, sem instanciar objeto!
        raw_data = Parser.extract_info(sys.argv[1])
        validated_data = Parser.parse_info(raw_data)
        
        print("=== PARSING E VALIDAÇÃO CONCLUÍDOS COM SUCESSO ===")
        print(validated_data)
    except ParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)