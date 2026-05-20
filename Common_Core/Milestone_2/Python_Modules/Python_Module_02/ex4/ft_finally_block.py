class PlantError(Exception):
    pass


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system(plants: list[str], label: str) -> bool:
    print(f"\nTesting {label}...")
    print("Opening watering system")
    try:
        for p in plants:
            water_plant(p)
        return True
    except PlantError as e:
        print(f"Caught PlantError: {e}")
        print(".. ending tests and returning to main")
        return False
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")

    test_watering_system(["Tomato", "Lettuce", "Carrots"], "valid plants")

    test_watering_system(["Tomato", "lettuce", "Carrots"], "invalid plants")

    print("\nCleanup always happens, even with errors!")
