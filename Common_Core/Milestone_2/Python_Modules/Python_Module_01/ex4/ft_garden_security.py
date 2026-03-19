
class SecurePlant():
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.__height = 0
        self.__age = 0
        self.initial_height = 0

    def set_height(self, height: int) -> None:
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected\n")
        else:
            self.__height = height
            print(f"Height updated: {self.__height}cm [OK]")

    def get_height(self) -> int:
        return self.__height

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected\n")
        else:
            self.__age = age
            print(f"Age updated: {self.__age} days [OK]\n")

    def get_age(self) -> int:
        return self.__age


if __name__ == "__main__":
    plant_data = [
        ("Rose", 25, 30),
    ]

    print("=== Garden Security System ===")
    plants = []

    for name, height, age in plant_data:
        plant = SecurePlant(name, 0, 0)
        print(f"Plant created: {plant.name}")
        plant.set_height(height)
        plant.set_age(age)
        plants.append(plant)

    plants[0].set_height(-5)

    for plant in plants:
        print(f"Current plant: {plant.name} "
              f"({plant.get_height()}cm, {plant.get_age()} days)")
