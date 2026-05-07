
import sys


def read(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def read_archives():
    if len(sys.argv) < 2:
        print("Usage: python3 ft_archive_creation.py <file>")
        exit(1)
    file = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{file}'")
    try:
        file_path = file
        text = read(file_path)
        print("Connection established...\n")
        print("RECOVERED DATA:")
        print("---\n")
        print(text)
        print("\n---")
        print("\nData recovery complete. Storage unit disconnected.")
        print(f"File '{file}' closed.")
    except FileNotFoundError as e:
        print(f"Error opening file '{file}': {e}")
        exit(1)
    except PermissionError as e:
        print(f"Error opening file '{file}': {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected ERROR: {e}")
        exit(1)


if __name__ == "__main__":
    try:
        read_archives()
    except Exception as e:
        print(e)
