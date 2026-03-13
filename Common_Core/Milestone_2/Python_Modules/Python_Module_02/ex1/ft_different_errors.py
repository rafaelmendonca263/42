
def garden_operations():
    print("Testing ValueError...")
    try:
        int("abc")
    except ValueError as error:
        print(f"Caught ValueError: {error}\n")
    print("Testing ZeroDivisionError...")
    try:
        res = 10 / 0
        print(res)
    except ZeroDivisionError as error:
        print(f"Caught ZeroDivisionError: {error}\n")
    print("Testing FileNotFoundError...")
    try:
        open('missing.txt')
    except FileNotFoundError as error:
        print(f"Caught FileNotFoundError: {error}\n")
    print("Testing KeyError...")
    try:
        plants["cactus"]
    except KeyError as error:
        print(f"Caught KeyError: {error}\n")
    print("Testing multiple exceptions together...")
    try:
        int("abc")
        res = 10 / 0
        print(res)
        open('missing.txt')
        plants["cactus"]
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught an error, but program continues!\n")


plants = {
    "rose": 25,
    "oak": 200,
}


def test_error_types():
    garden_operations()
    print("All error types tested successfully!")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")
    test_error_types()
