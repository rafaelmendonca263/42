
from ex3.GameEngine import GameEngine
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory


if __name__ == "__main__":
    print("=== DataDeck Game Engine ===")

    print("Configuring Fantasy Card Game...")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()

    engine = GameEngine()
    engine.configure_engine(factory, strategy)

    print("Factory:", factory.__class__.__name__)
    print("Strategy:", strategy.__class__.__name__)
    print("Available types:", factory.get_supported_types())

    print("Simulating aggressive turn...")

    result = engine.simulate_turn()

    print("Hand: [" + ", ".join(result["hand"]) + "]")

    print("Turn execution:")
    print("Strategy:", result["strategy"])
    print("Actions:", result["actions"])

    print("Game Report:")
    print(engine.get_engine_status())

    print("Abstract Factory + Strategy Pattern:"
          " Maximum flexibility achieved!")
