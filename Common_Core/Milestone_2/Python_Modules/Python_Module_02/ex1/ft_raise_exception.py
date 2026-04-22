
def check_temperature(temp_str: str) -> None:
    print(f"Imput data is '{temp_str}'")
    try:
        temp = int(temp_str)
        if temp > 0 and temp < 40:
            print(f"Temperature is now {temp}°C")
        elif temp > 40:
            print(f"Caught input_temperature error: {temp}°C is too hot "
                  "for plants (max 40°C)C")
        elif temp < 0:
            print(f"Caught input_temperature error: {temp}°C is too cold "
                  "for plants (min 0°C)")
    except ValueError:
        print(f"Caught input_temperature error: invalid literal for "
              f"int() with base 10: '{temp_str}'")


def test_temperature_input() -> None:
    check_temperature("25")
    print("")
    check_temperature("abc")
    print("")
    check_temperature("100")
    print("")
    check_temperature("-25")
    print("")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    test_temperature_input()
    print("All tests completed - program didn't crash!")
