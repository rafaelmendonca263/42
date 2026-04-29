
import sys

def read_lines(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
            return file.readlines()

def process_archives():
    if len(sys.argv) < 2:
        print("Uso: python3 ft_archive_creation.py <nome_do_ficheiro>")
        return
    
    file_name = sys.argv[1]
    
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")
    print("---")
    
    new_lines = []
    try:
        lines = read_lines(file_name)
        for line in lines:
            cleaned_line = line.rstrip('\n')
            print(cleaned_line)
            new_lines.append(cleaned_line + "#")
        print("---")
        print(f"File '{file_name}' closed.")
        print("Transform data:")
        print("---")

        for line in new_lines:
            print(line)
        print("---")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return
    
    new_name = input("Enter new file name (or empty): ").strip()
    
    if new_name:
        print(f"Saving data to '{new_name}'")
        with open(new_name, "w", encoding="utf-8") as f_out:
            for linha in new_lines:
                f_out.write(linha + "\n")
        print(f"Data saved in file '{new_name}'.")
    else:
        print("No file name provided. Aborting save.")

if __name__ == "__main__":
    process_archives()