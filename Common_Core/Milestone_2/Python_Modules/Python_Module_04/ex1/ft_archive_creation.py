
def write_archive(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)
    return text


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    print("Initializing new storage unit: new_discovery.txt")
    try:
        file_path = 'new_discovery.txt'
        text = write_archive(file_path, "[ENTRY 001] New quantum "
                                        "algorithm discovered\n"
                                        "[ENTRY 002] Efficiency increased "
                                        "by 347%\n"
                                        "[ENTRY 003] Archived by "
                                        "Data Archivist trainee")
        print("Storage unit created successfully...\n")
        print("Inscribing preservation data...")
        print(text)
        print("\nData inscription complete. Storage unit sealed.")
        print("Archive 'new_discovery.txt' ready for long-term preservation.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
