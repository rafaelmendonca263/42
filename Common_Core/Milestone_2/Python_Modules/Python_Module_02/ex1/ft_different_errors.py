
def garden_operations() -> None:
    print("Testing ValueError...")
    try:
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")
    print("\nTesting ZeroDivisionError...")
    try:
        res = 10 / 0
        print(res)
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero")
    print("\nTesting FileNotFoundError...")
    try:
        open('missing.txt')
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file 'missing.txt'")
    print("\nTesting KeyError...")
    try:
        plants["cactus"]
    except KeyError:
        print("Caught KeyError: 'cactus'")
    print("\nTesting multiple exceptions together...")
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


def test_error_types() -> None:
    garden_operations()
    print("All error types tested successfully!")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")
    test_error_types()
