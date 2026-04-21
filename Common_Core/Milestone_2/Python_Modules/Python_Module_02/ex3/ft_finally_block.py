
class GardenError(Exception):
    """Erro básico para problemas no jardim."""
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    """Erro para problemas com plantas."""
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    """Erro para problemas com rega."""
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def check_plant(name: str) -> None:
    if name == "tomato":
        raise PlantError(f"The {name} plant is wilting!")


def check_water(level: int) -> None:
    if level < 10:
        raise WaterError("Not enough water in the tank!")


def garden_custom_errors_demo() -> None:
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
        print(f"Caught GardenError: {e}")

    try:
        check_water(5)
    except GardenError as e:
        print(f"Caught GardenError: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    garden_custom_errors_demo()
    print("\nAll custom error types work correctly!")
