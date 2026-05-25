from collections import abc


def spell_combiner(
    spell1: abc.Callable[[str, int], str],
    spell2: abc.Callable[[str, int], str]
) -> abc.Callable[[str, int], tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))

    return combined


def power_amplifier(
    base_spell: abc.Callable[[str, int], str],
    multiplier: int
) -> abc.Callable[[str, int], str]:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(
    condition: abc.Callable[[str, int], bool],
    spell: abc.Callable[[str, int], str]
) -> abc.Callable[[str, int], str]:
    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return caster


def spell_sequence(
    spells: list[abc.Callable[[str, int], str]]
) -> abc.Callable[[str, int], list[str]]:
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def main() -> None:
    def fireball(target: str, power: int) -> str:
        return f"Fireball hits {target} for {power} damage"

    def heal(target: str, power: int) -> str:
        return f"Heal restores {target} for {power} HP"

    def is_dragon(target: str, power: int) -> bool:
        return target.lower() == "dragon"

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    print(f"Combined spell result: {combined('Dragon', 20)}")

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: 10, Amplified power simulation through function:")
    print(mega_fireball("Orc", 10))


if __name__ == "__main__":
    main()