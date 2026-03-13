
def check_temperature(temp_str: str):
    print(f"Testing temperature: {temp_str}")
    try:
        temp = int(temp_str)
        if temp > 0 and temp < 40:
            print("Temperature 25°C is perfect for plants!")
        elif temp > 40:
            print(f"Error: {temp}°C is too hot for plants (max 40°C)")
        elif temp < 0:
            print(f"Error: {temp}°C is too cold for plants (min 0°C)")
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")


def test_temperature_input():
    check_temperature("25")
    print("")
    check_temperature("abc")
    print("")
    check_temperature("100")
    print("")
    check_temperature("-25")
    print("")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature_input()
    print("All tests completed - program didn't crash!")
