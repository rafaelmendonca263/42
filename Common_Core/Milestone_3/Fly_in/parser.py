def parse_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue

            part = line.split(":")
            type = part[0].strip()
            data = part[1].strip()
            
            print(f"Instrução: {type} | data: {data}")

parse_file("file.txt")