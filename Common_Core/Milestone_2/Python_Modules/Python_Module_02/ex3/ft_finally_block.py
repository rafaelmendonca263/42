
class PlantError(Exception):
    pass


def check_plant(plant):
    if plant is None:
        raise PlantError("Cannot water None - invalid plant!")


def water_plants(plant_list):
    print("Opening watering system")
    success = True

    try:
        for plant in plant_list:
            check_plant(plant)
            print(f"Watering {plant}")
    except PlantError as e:
        success = False
        print(f"Error: {e}")
    finally:
        print("Closing watering system (cleanup)")
        if success:
            print("Watering completed successfully!\n")
        else:
            print("Cleanup always happens, even with errors!\n")


def test_watering_system():
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])

    print("Testing with error...")
    water_plants(["tomato", None, "carrots"])


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    test_watering_system()
