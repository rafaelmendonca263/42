
class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


class WaterError(GardenError):
    pass


def check_plant(plant_name):
    if plant_name == "tomato":
        raise PlantError(f"The {plant_name} plant is wilting!")


def check_water(level):
    if level < 10:
        raise WaterError("Not enough water in the tank!")


def garden_custom_errors_demo():
    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print()

    print("Testing WaterError...")
    try:
        check_water(5)
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print()

    print("Testing catching all garden errors...")
    try:
        check_plant("tomato")
    except GardenError as e:
        print(f"Caught a garden error: {e}")
    try:
        check_water(5)
    except GardenError as e:
        print(f"Caught a garden error: {e}")
    print()

    print("All custom error types work correctly!")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    garden_custom_errors_demo()
