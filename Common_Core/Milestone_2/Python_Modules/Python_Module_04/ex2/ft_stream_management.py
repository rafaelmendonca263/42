
import sys

def read_lines(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
                return file.readlines()
    except FileNotFoundError as e:
        print(f"[STDERR] Error opening file '{file_path}': {e} ", file=sys.stderr)
        exit()

def process_archives():
    if len(sys.argv) < 2:
        print("Uso: python3 ft_stream_management.py <nome_do_ficheiro>", file=sys.stderr)
        return
    
    file_name = sys.argv[1]
    
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")
    print("---\n")
    
    new_lines = []
    try:
        lines = read_lines(file_name)
        for line in lines:
            cleaned_line = line.rstrip('\n')
            print(cleaned_line)
            new_lines.append(cleaned_line + "#")
        print("\n---")
        print(f"File '{file_name}' closed.\n")
        print("Transform data:")
        print("---\n")

        for line in new_lines:
            print(line)
        print("\n---")
    except Exception as e:
        print(f"[STDERR] Unexpected error: {e}", file=sys.stderr)
        exit()
    
    new_name = sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    resposta = sys.stdin.readline()
    new_name = resposta.strip()

    if new_name:
        print(f"Saving data to '{new_name}'")
        try:
            with open(new_name, "w", encoding="utf-8") as f_out:
                for linha in new_lines:
                    f_out.write(linha + "\n")
            print(f"Data saved in file '{new_name}'.")
        except Exception as e:
            print(f"[STDERR] Error opening file '{new_name}': {e}", file=sys.stderr)
            print("Data not saved.")
    else:
            print("Data not saved.")

if __name__ == "__main__":
    process_archives()