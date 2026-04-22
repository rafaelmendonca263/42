
class Plant():
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age
        self.initial_height = height

    def grow(self, cm: int) -> None:
        self.height += cm

    def age_one_day(self) -> None:
        self.age += 1

    def get_info(self) -> str:
        return f"{self.name}: {self.height}cm, {self.age} days old"


rose = Plant("Rose", 25, 30)
sunflower = Plant("Sunflower", 80, 45)
cactus = Plant("Cactus", 15, 120)

plants = [rose, sunflower, cactus]

if __name__ == "__main__":
    for day in range(1, 8):
        print(f"=== Day{day} ===")
        for plant in plants:
            plant.grow(3)
            plant.age_one_day()
            print(plant.get_info())
    growth = plant.height - plant.initial_height
    print(f"Growth this week: +{growth}cm")
