
class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age
        self.initial_height = height  

    def grow(self, cm):
        self.height += cm

    def age_one_day(self):
        self.age += 1

    def get_info(self):
        return f"{self.name}: {self.height}cm, {self.age} days old"

plant_data = [
    ("Rose", 25, 30),
    ("Oak", 200, 365),
    ("Cactus", 5, 90),
    ("Sunflower", 80, 45),
    ("Fern", 15, 120)
]

if __name__ == "__main__":
    plants = []
    for name, height, age in plant_data:
        plant = Plant(name, height, age)
        plants.append(plant)
        print(f"Created: {plant.get_info()}")
    print(f"Total plants created: {len(plants)}")