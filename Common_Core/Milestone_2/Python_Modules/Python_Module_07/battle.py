from ex0 import FlameFactory, AquaFactory, CreatureFactory, Creature


def verify_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base: Creature = factory.create_base()
    evolved: Creature = factory.create_evolved()

    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def run_battle(factory_f: CreatureFactory, factory_a: CreatureFactory) -> None:
    print("Testing battle")
    fire_base: Creature = factory_f.create_base()
    water_base: Creature = factory_a.create_base()

    print(fire_base.describe())
    print(" VS.")
    print(water_base.describe())
    print(" fight!")
    print(fire_base.attack())
    print(water_base.attack())


if __name__ == "__main__":
    try:
        flame_fact = FlameFactory()
        aqua_fact = AquaFactory()

        verify_factory(flame_fact)
        print()
        verify_factory(aqua_fact)
        print()
        run_battle(flame_fact, aqua_fact)
    except Exception as e:
        print(e)
