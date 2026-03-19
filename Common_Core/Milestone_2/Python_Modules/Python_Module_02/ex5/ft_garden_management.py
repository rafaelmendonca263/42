
class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


class WaterError(GardenError):
    pass


class Plant:
    def __init__(self,
                 name: str,
                 water_level: int,
                 sunlight_hours: int) -> None:
        if not name:
            raise PlantError("Plant name cannot be empty!")
        self.name = name
        self.water_level = water_level
        self.sunlight_hours = sunlight_hours


class GardenManager:
    def __init__(self) -> None:
        self.plants: list[Plant] = []

    def add_plant(self,
                  name: str,
                  water_level: int,
                  sunlight_hours: int) -> None:
        try:
            plant = Plant(name, water_level, sunlight_hours)
            self.plants.append(plant)
            print(f"Added {name} successfully")
        except PlantError as e:
            print(f"Error adding plant: {e}")

    def water_plants(self) -> None:
        print("Opening watering system")
        try:
            for plant in self.plants:
                try:
                    if plant.water_level < 2:
                        raise WaterError(
                            f"Error checking {plant.name}: "
                            f"Water level {plant.water_level} "
                            "is too low (min 2)"
                        )
                    print(f"Watering {plant.name} - success")
                except WaterError as e:
                    print(f"Caught GardenError: {e}")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self) -> None:
        for plant in self.plants:
            try:
                if plant.water_level > 10:
                    raise PlantError(f"Water level {plant.water_level} "
                                     "is too high (max 10)")
                if plant.water_level < 1:
                    raise PlantError(f"Water level {plant.water_level} "
                                     "is too low (min 1)")
                print(f"{plant.name}: healthy (water: {plant.water_level},"
                      f" sun: {plant.sunlight_hours})")
            except PlantError as e:
                print(f"Error checking {plant.name}: {e}")


def test_garden_management() -> None:
    print("Adding plants to garden...")
    garden = GardenManager()
    garden.add_plant("tomato", 5, 8) 
    garden.add_plant("lettuce", 15, 6)
    garden.add_plant("", 4, 5)

    print("\nWatering plants...")
    garden.water_plants()

    print("\nChecking plant health...")
    garden.check_plant_health()

    print("\nTesting error recovery...")
    try:
        raise WaterError("Not enough water in tank")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")


if __name__ == "__main__":
    print("=== Garden Management System ===\n")
    test_garden_management()
