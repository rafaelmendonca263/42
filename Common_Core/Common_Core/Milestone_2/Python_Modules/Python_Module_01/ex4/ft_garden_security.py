class SecurePlant:
    def __init__(self, name, height, age):
        self.name = name
        self._height = 0  
        self._age = 0
        self.initial_height = 0

    def set_height(self, height):
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self._height = height
            print(f"Height updated: {self._height}cm [OK]")

    def get_height(self):
        return self._height

    def set_age(self, age):
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self._age = age
            print(f"Age updated: {self._age} days [OK]")

    def get_age(self):
        return self._age


if __name__ == "__main__":
    plant_data = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120)
    ]

    print("=== Garden Security System ===")
    plants = []

    for name, height, age in plant_data:
        plant = SecurePlant(name, 0, 0)
        print(f"Plant created: {plant.name}")
        plant.set_height(height)
        plant.set_age(age)
        plants.append(plant)

    print("\n--- Testing updates ---\n")
    plants[0].set_height(-5)
    plants[0].set_age(-10)

    print("\n--- Current plant states ---\n")
    for plant in plants:
        print(f"Current plant: {plant.name} ({plant.get_height()}cm, {plant.get_age()} days)")
