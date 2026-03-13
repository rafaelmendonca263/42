
def crisis_response():
    print("CRISIS ALERT: Attempting access to 'lost_archive.txt'...")
    try:
        with open("lost_archive.txt", "r") as f:
            content = f.read()
            print("SUCCESS: Archive recovered - ``Knowledge "
                  "preserved for humanity''")
            print("STATUS: Normal operations resumed\n")
            print(content)
    except FileNotFoundError:
        print("CRISIS ALERT: 'lost_archive.txt' not found.\n")
    except PermissionError:
        print("CRISIS ALERT: Permission denied for 'lost_archive.txt'.\n")
    except Exception as e:
        print(f"CRISIS ALERT: An unexpected error occurred: {e}\n")

    print("CRISIS ALERT: Attempting access to 'classified_vault.txt'...")
    try:
        with open("classified_vault.txt", "r") as f:
            content = f.read()
            print("SUCCESS: Archive recovered - ``Knowledge "
                  "preserved for humanity''")
            print("STATUS: Normal operations resumed\n")
    except FileNotFoundError:
        print("CRISIS ALERT: 'classified_vault.txt' not found.\n")
    except PermissionError:
        print("CRISIS ALERT: Permission denied for 'classified_vault.txt'.\n")
    except Exception as e:
        print(f"CRISIS ALERT: An unexpected error occurred: {e}\n")

    print("ROUTINE ACCESS: Attempting access to 'standard_archive.txt'...")
    try:
        with open("standard_archive.txt", "r") as f:
            content = f.read()
            print("SUCCESS: Archive recovered - ``Knowledge preserved"
                  " for humanity''")
            print("STATUS: Normal operations resumed\n")
    except FileNotFoundError:
        print("CRISIS ALERT: 'standard_archive.txt' not found.\n")
    except PermissionError:
        print("CRISIS ALERT: Permission denied for 'standard_archive.txt'.\n")
    except Exception as e:
        print(f"CRISIS ALERT: An unexpected error occurred: {e}\n")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")
    crisis_response()
    print("All crisis scenarios handled successfully. Archives secure.")
