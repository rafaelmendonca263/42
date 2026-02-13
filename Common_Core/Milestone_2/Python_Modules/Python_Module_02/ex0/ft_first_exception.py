
def check_temperature(temp_str: str):
    print(f"Testing temperature: {temp_str}")
    try:
        temp = int(temp_str)
        if temp > 0 and temp < 40:
            print(f"Temperature 25°C is perfect for plants!")
        elif temp > 40:
            print(f"Error: {temp}°C is too hot for plants (max 40°C)")
        elif temp < 0:
            print(f"Error: {temp}°C is too cold for plants (min 0°C)")
    except:
        print(f"Error: '{temp_str}' is not a valid number")

def  test_temperature_input():
    check_temperature("25")
    print(f"")
    check_temperature("abc")
    print(f"")
    check_temperature("100")
    print(f"")
    check_temperature("-25")
    print(f"")

if __name__=="__main__":
    print(f"=== Garden Temperature Checker ===")
    test_temperature_input()
    print(f"All tests completed - program didn't crash!")