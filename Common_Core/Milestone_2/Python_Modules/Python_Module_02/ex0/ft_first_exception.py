def check_temperature(temp_str: str) -> None:
    print(f"Imput data is '{temp_str}'")
    try:
        temp = int(temp_str)
        print(f"Temperature is now {temp}°C")
    except ValueError:
        print(
            "Caught input_temperature error: invalid literal for "
            f"int() with base 10: '{temp_str}'"
        )


def test_temperature_input() -> None:
    check_temperature("25")
    print("")
    check_temperature("abc")
    print("")


if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    test_temperature_input()
    print("All tests completed - program didn't crash!")
