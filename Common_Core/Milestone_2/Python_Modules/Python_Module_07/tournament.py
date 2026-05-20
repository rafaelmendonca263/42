from typing import List, Tuple
from ex0 import FlameFactory, AquaFactory, CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    StrategyValidationError,
)


def run_tournament(
    label: str, opponents: List[Tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print(label)

    fact_names = []
    for f, s in opponents:
        name = f.__class__.__name__.replace("CreatureFactory", "").replace(
            "Factory", ""
        )
        strat = s.__class__.__name__.replace("Strategy", "")
        fact_names.append(f"({name}+{strat})")

    print(f" [ {', '.join(fact_names)} ]")
    print(" *** Tournament ***")
    print(f" {len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            fact1, strat1 = opponents[i]
            fact2, strat2 = opponents[j]

            c1 = fact1.create_base()
            c2 = fact2.create_base()

            print("\n * Battle *")
            print(f" {c1.describe()}")
            print(" vs.")
            print(f" {c2.describe()}")
            print(" now fight!")

            try:
                print(strat1.act(c1))
                print(strat2.act(c2))
            except StrategyValidationError as e:
                print(f" Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    try:
        flame_f = FlameFactory()
        aqua_f = AquaFactory()
        healing_f = HealingCreatureFactory()
        transform_f = TransformCreatureFactory()

        normal_s = NormalStrategy()
        aggressive_s = AggressiveStrategy()
        defensive_s = DefensiveStrategy()

        run_tournament(
            "Tournament 0 (basic)",
            [(flame_f, normal_s), (healing_f, defensive_s)],
        )
        print()
        run_tournament(
            "Tournament 1 (error)",
            [(flame_f, aggressive_s), (healing_f, defensive_s)],
        )
        print()
        run_tournament(
            "Tournament 2 (multiple)",
            [
                (aqua_f, normal_s),
                (healing_f, defensive_s),
                (transform_f, aggressive_s),
            ],
        )
    except Exception as e:
        print(e)
