
def display_stats(plant: 'Plant') -> None:
    """Função única global para exibir estatísticas de qualquer planta."""
    plant.display_internal_stats()


class Plant:
    class Stats:
        """Classe aninhada para segurar dados estatísticos."""
        def __init__(self) -> None:
            self.grow_calls: int = 0
            self.age_calls: int = 0
            self.show_calls: int = 0

    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age
        self._stats = self.Stats()

    def grow(self, cm: float) -> None:
        self.height += cm
        self._stats.grow_calls += 1

    def age_days(self, days: int) -> None:
        self.age += days
        self._stats.age_calls += 1

    def show(self) -> None:
        self._stats.show_calls += 1
        print(f"{self.name}: {self.height}cm, {self.age} days old")

    def display_internal_stats(self) -> None:
        print(f"Stats: {self._stats.grow_calls} grow, "
              f"{self._stats.age_calls} age, "
              f"{self._stats.show_calls} show")

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        """Verifica se a idade é superior a um ano."""
        return age > 365

    @classmethod
    def create_anonymous(cls) -> 'Plant':
        """Cria uma planta anónima diretamente."""
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color = color
        self.is_blooming = False

    def bloom(self) -> None:
        self.is_blooming = True
        print(f"{self.name} is blooming beautifully!")

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.is_blooming:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Seed(Flower):
    """Classe Seed que herda de Flower e guarda número de sementes."""
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age, color)
        self.seed_count = 0

    def bloom(self) -> None:
        super().bloom()
        self.seed_count = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seed_count}")


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        self.shade_calls = 0

    def produce_shade(self) -> None:
        self.shade_calls += 1
        print(f"Tree {self.name} now produces a shade of "
              f"{self.height}cm long and {self.trunk_diameter}cm wide.")

    def display_internal_stats(self) -> None:
        """Override para incluir chamadas de sombra."""
        super().display_internal_stats()
        print(f"{self.shade_calls} shade")


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("\n=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_stats(rose)

    print("[asking the rose to grow and bloom]")
    rose.grow(8)
    rose.bloom()
    rose.show()
    display_stats(rose)

    print("\n=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_stats(oak)

    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)

    print("\n=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()

    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30)
    sunflower.age_days(20)
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)

    print("\n=== Anonymous")
    anon = Plant.create_anonymous()
    anon.show()
    display_stats(anon)
