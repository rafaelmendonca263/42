from ex3.GameEngine import GameEngine
from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory


if __name__ == "__main__":
    print("\n=== DataDeck Game Engine ===")

    print("\nConfiguring Fantasy Card Game...")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()

    engine = GameEngine()
    engine.configure_engine(factory, strategy)

    print("Factory:", factory.__class__.__name__)
    print("Strategy:", strategy.__class__.__name__)
    print("Available types:", factory.get_supported_types())

    print("\nSimulating aggressive turn...")

    result = engine.simulate_turn()

    print("\nTurn execution:")
    print("Strategy:", result["strategy"])
    print("Actions:", result["actions"])

    print("\nGame Report:")
    print(engine.get_engine_status())
