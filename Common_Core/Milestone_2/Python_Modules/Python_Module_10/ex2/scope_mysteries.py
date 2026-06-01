from collections import abc
from typing import Any


def mage_counter() -> abc.Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> abc.Callable[[int], int]:
    total_power = initial_power

    def accumulator(power: int) -> int:
        nonlocal total_power
        total_power += power
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> abc.Callable[[str], str]:
    def enchanter(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchanter


def memory_vault() -> dict[str, abc.Callable[..., Any]]:
    vault: dict[str, str | int] = {}

    def store(key: str, value: str | int) -> None:
        vault[key] = value

    def recall(key: str) -> str | int:
        if key in vault:
            return vault[key]
        return "Memory not found"

    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")
    print(f"Base 100, add 30: {acc(30)}")

    print("\nTesting enchantment factory...")
    flame_enchant = enchantment_factory("Flaming")
    frost_enchant = enchantment_factory("Frozen")
    print(flame_enchant("Sword"))
    print(frost_enchant("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == "__main__":
    main()
