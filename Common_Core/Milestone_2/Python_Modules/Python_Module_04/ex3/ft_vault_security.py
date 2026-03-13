
def secure_read_vault():
    print("Initiating secure vault access...")
    with open("classified_data.txt", "r") as f:
        print("Vault connection established with failsafe protocols.\n")
        content = f.read()
        print("SECURE EXTRACTION:")
        print(content + "\n")


def secure_write_vault():
    with open("classified_data.txt", "w") as f:
        print("SECURE PRESERVATION:")
        f.write("[CLASSIFIED] New security protocols archived")
    print("Vault automatically sealed upon completion\n")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")

    secure_read_vault()
    secure_write_vault()

    print("All vault operations completed with maximum security.")
