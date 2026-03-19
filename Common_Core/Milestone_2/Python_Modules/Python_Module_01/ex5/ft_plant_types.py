
import math


class Plant():
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color

    def describe(self):
        print(f"{self.name} (Flower): {self.height}cm, "
              f"{self.age} days, {self.color} color")

    def bloom(self):
        print(f"{self.name} is blooming beautifully!\n")


class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, trunk_diameter: int):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def describe(self):
        print(f"{self.name} (Tree): {self.height}cm, "
              f"{self.age} days, {self.trunk_diameter}cm diameter")

    def produce_shade(self):
        radius = self.trunk_diameter / 2
        shade_area = math.pi * (radius ** 2)
        print(f"{self.name} provides {int(shade_area)} "
              "square meters of shade\n")


class Vegetable(Plant):
    def __init__(
            self,
            name: str,
            height: int,
            age: int,
            harvest_season: str,
            nutritional_value: str):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def describe(self):
        print(f"{self.name} (Vegetable): {self.height}cm,"
              f" {self.age} days, {self.harvest_season} harvest")

    def nutrition(self):
        print(f"{self.name} is rich in {self.nutritional_value}\n")


if __name__ == "__main__":
    print("=== Garden Plant Types ===\n")

    # Flowers
    flower1 = Flower("Rose", 25, 30, "red")
    flower2 = Flower("Tulip", 20, 25, "yellow")

    # Trees
    tree1 = Tree("Oak", 500, 1825, 10)
    tree2 = Tree("Pine", 600, 2000, 12)

    # Vegetables
    veg1 = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    veg2 = Vegetable("Carrot", 30, 70, "winter", "vitamin A")

    # Output
    flower1.describe()
    flower1.bloom()
    flower2.describe()
    flower2.bloom()

    tree1.describe()
    tree1.produce_shade()
    tree2.describe()
    tree2.produce_shade()

    veg1.describe()
    veg1.nutrition()
    veg2.describe()
    veg2.nutrition()
