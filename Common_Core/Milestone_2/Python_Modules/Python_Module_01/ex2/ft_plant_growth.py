
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

rose = Plant("Rose", 25, 30)
sunflower = Plant("Sunflower", 80, 45)
cactus = Plant("Cactus", 15, 120)

plants = [rose, sunflower, cactus]

if __name__ == "__main__":
    print("=== Day 1 ===")
    for plant in plants:
        print(plant.get_info())
    for day in range(2, 8):
        for plant in plants:
            plant.grow(3)
            plant.age_one_day()
    print("=== Day 7 ===")
    for plant in plants:
        print(plant.get_info())
        growth = plant.height - plant.initial_height
        print(f"Growth this week: +{growth}cm\n")
