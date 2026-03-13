
import alchemy.transmutation
from alchemy.transmutation.advanced import philosophers_stone, elixir_of_life
from alchemy.transmutation.basic import lead_to_gold, stone_to_gem

if "__main__" == __name__:

    print("\n=== Pathway Debate Mastery ===")

    print("\nTesting Absolute Imports (from basic.py):")

    print(f"lead_to_gold(): {lead_to_gold()}")
    print(f"stone_to_gem(): {stone_to_gem()}")

    print("\nTesting Relative Imports (from advanced.)")
    print(f"philosopheres_stone(): {philosophers_stone()}")
    print(f"elixir_of_life(): {elixir_of_life()}")

    print("\nTesting Package Access:")
    print("alchemy.transmutation.lead_to_gold(): "
          f"{alchemy.transmutation.lead_to_gold()}")
    print(f"alchemy.transmutation.philosophers_stone():"
          f" {alchemy.transmutation.philosophers_stone()}")

    print("\nBoth pathways work! Absolute: clear, Relative: concise")
