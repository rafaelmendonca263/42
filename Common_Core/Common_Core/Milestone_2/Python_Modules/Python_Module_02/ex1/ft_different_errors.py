
def garden_operations():
    try:
        print(f"Testing ValueError...")
        try:
            int("abc")
        except ValueError as error:
            print(f"Caught ValueError: {error}\n")
        print("Testing ZeroDivisionError...")
        try:
            res = 10 / 0
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
            open('missing.txt')
            plants["cactus"]
        except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError) as error:
            print(f"Caught an error, but program continues!\n")
    except:
        print("An unexpected error occurred.\n")

plants = {
    "rose": 25,
    "oak": 200,
}

def test_error_types():
    garden_operations()
    print(f"All error types tested successfully!")


if __name__=="__main__":
    print(f"=== Garden Error Types Demo ===\n")
    test_error_types()