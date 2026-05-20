def secure_archive(file_name, action="r", content=None):
    try:
        if action == "r":
            with open(file_name, "r") as file:
                data = file.read()
            return (True, data)

        elif action == "w":
            with open(file_name, "w") as file:
                if content is not None:
                    file.write(content)
            return (True, "Content successfully written to file")

        else:
            return (False, f"Invalid action: '{action}'. Use 'r' or 'w'.")

    except Exception as e:
        return (False, str(e))


if __name__ == "__main__":
    try:
        print("=== Cyber Archives Security ===\n")

        print("Using 'secure_archive' to read from a nonexistent file:")
        print(secure_archive("/not/existing/file", "r"))

        print("\nUsing 'secure_archive' to read from an inaccessible file:")
        print(secure_archive("/etc/shadow", "r"))

        archive_data = (
            "[FRAGMENT 001] Digital preservation protocols established 2087\n"
            "[FRAGMENT 002] Knowledge must survive the entropy wars\n"
            "[FRAGMENT 003] Every byte saved is a victory against oblivion\n"
        )

        print(
            "\nUsing 'secure_archive' to write previous content"
            " to a new file:"
        )
        print(secure_archive("cyber_archive_log.txt", "w", archive_data))

        print("\nUsing 'secure_archive' to read from a regular file:")
        print(secure_archive("cyber_archive_log.txt", "r"))

    except Exception as e:
        print(e)
