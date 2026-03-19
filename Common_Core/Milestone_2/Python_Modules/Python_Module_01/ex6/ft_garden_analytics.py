
class Plant:
    def __init__(self, name: str, height: int) -> None:
        self.name = name
        self.height = height

    def grow(self) -> None:
        self.height += 1
        print(f"{self.name} grew 1cm")

    def describe(self) -> str:
        return f"- {self.name}: {self.height}cm"


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, color: str) -> None:
        super().__init__(name, height)
        self.color = color
        self.blooming = True

    def describe(self) -> str:
        return (f"- {self.name}: {self.height}cm, "
                f"{self.color} flowers (blooming)")


class PrizeFlower(FloweringPlant):
    def __init__(self,
                 name: str,
                 height: int,
                 color: str,
                 points: int) -> None:
        super().__init__(name, height, color)
        self.points = points

    def describe(self) -> str:
        return (f"- {self.name}: {self.height}cm, {self.color} flowers "
                f"(blooming), Prize points: {self.points}")


class Garden:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.plants = []
        self.total_growth = 0

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self) -> None:
        print(f"\n{self.owner} is helping all plants grow...")
        for plant in self.plants:
            plant.grow()
            self.total_growth += 1

    def report(self) -> None:
        print(f"\n=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(plant.describe())

    def calculate_score(self) -> int:
        score = 0
        for plant in self.plants:
            if isinstance(plant, PrizeFlower):
                score += 30
            elif isinstance(plant, FloweringPlant):
                score += 20
            else:
                score += 10
        return score


class GardenManager:
    total_gardens = 0

    class GardenStats:
        def __init__(self, garden: Garden) -> None:
            self.garden = garden

        def calculate(self) -> None:
            regular = 0
            flowering = 0
            prize = 0

            for plant in self.garden.plants:
                if isinstance(plant, PrizeFlower):
                    prize += 1
                elif isinstance(plant, FloweringPlant):
                    flowering += 1
                else:
                    regular += 1

            print(f"Plants added: {len(self.garden.plants)}, "
                  f"Total growth: {self.garden.total_growth}cm")
            print(f"Plant types: {regular} regular, {flowering} flowering, "
                  f"{prize} prize flowers")

    def __init__(self) -> None:
        self.gardens = []
        GardenManager.total_gardens += 1

    def add_garden(self, garden: Garden) -> None:
        self.gardens.append(garden)

    def analyze(self) -> None:
        for garden in self.gardens:
            garden.report()
            stats = GardenManager.GardenStats(garden)
            stats.calculate()

    @classmethod
    def create_garden_network(cls):
        return cls()

    @staticmethod
    def validate_height(height: int) -> bool:
        return height > 0


# === MAIN ===
if __name__ == "__main__":
    print("=== Garden Management System Demo ===\n")

    manager = GardenManager.create_garden_network()

    garden1 = Garden("Alice")
    garden2 = Garden("Bob")

    manager.add_garden(garden1)
    manager.add_garden(garden2)

    # Plants
    oak = Plant("Oak Tree", 100)
    rose = FloweringPlant("Rose", 25, "red")
    sunflower = PrizeFlower("Sunflower", 50, "yellow", 10)
    dandelion = PrizeFlower("Dandelion", 250, "blue", 5)

    garden1.add_plant(oak)
    garden1.add_plant(rose)
    garden1.add_plant(sunflower)
    garden2.add_plant(dandelion)

    garden1.grow_all()
    garden2.grow_all()

    manager.analyze()

    print(f"\nHeight validation test: {GardenManager.validate_height(10)}")

    alice_score = garden1.calculate_score()
    bob_score = garden2.calculate_score()
    print(f"Garden scores - Alice: {alice_score}, Bob: {bob_score}")

    print(f"Total gardens managed: {len(manager.gardens)}")
