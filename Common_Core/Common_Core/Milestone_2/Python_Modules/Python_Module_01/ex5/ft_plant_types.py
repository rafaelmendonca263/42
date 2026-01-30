
class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age
    
    def get_info(self):
        return f"{self.name}: {self.height}cm, {self.age} days old"
    
class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        print(f"{self.name} is blooming beautifully!")

    
class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self):
        shade = int(self.trunk_diameter * 1.56)
        print(f"{self.name} provides {shade} square meters of shade")


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

if __name__ == "__main__":
    print("=== Garden Plant Types ===\n")
    rose = Flower("Rose", 25, 30, "red")
    sunflower = Flower("Sunflower", 80, 45, "yellow")

    oak = Tree("Oak", 500, 1825, 50)
    olive_tree = Tree("Olive Tree", 300, 1000, 40)

    tomato = Vegetable("Tomato", 80, 90, "summer", "rich in vitamin C")
    carrot = Vegetable("Carrot", 30, 60, "fall", "rich in beta-carotene")
    plants = [rose, sunflower, oak, olive_tree, tomato, carrot]
    for plant in plants:
        print(f"{plant.name} ({plant.__class__.__name__}): {plant.get_info()}", end="")

        if isinstance(plant, Flower):
            print(f", {plant.color} color")
            plant.bloom()
        elif isinstance(plant, Tree):
            print(f", {plant.trunk_diameter}cm diameter")
            plant.produce_shade()
        elif isinstance(plant, Vegetable):
            print(f", {plant.harvest_season} harvest")
            print(f"{plant.name} is {plant.nutritional_value}")
        print()