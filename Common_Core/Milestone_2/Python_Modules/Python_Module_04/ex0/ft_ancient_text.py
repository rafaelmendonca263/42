
def read(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

if __name__ == "__main__":
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    print("Accessing Storage Vault: ancient_fragment.txt")
    try:
        file_path = 'ancient_fragment.txt'
        text = read(file_path)
        print("Connection established...\n")
        print("RECOVERED DATA:")
        print(text)
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")