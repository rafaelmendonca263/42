def spell_combiner(spell1: callable, spell2: callable) -> callable:
    def new_wand(*args, **kwargs):
        spell_combined = (spell1(*args, **kwargs), spell2(*args, **kwargs))
        return spell_combined
    return new_wand


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    def amplified_spell(*args, **kwargs):
        base_power = base_spell(*args, **kwargs)
        return base_power * multiplier
    return amplified_spell


def conditional_caster(condition: callable, spell: callable) -> callable:
    def conditional_spell(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        else:
            return "Spell fizzled"
    return conditional_spell


def spell_sequence(spells: list[callable]) -> callable:
    def sequence_caster(*args, **kwargs):
        results = []
        for spell in spells:
            result = spell(*args, **kwargs)
            results.append(result)
        return results
    return sequence_caster


if __name__ == "__main__":
    # 1. Criar alguns feitiços base para testar
    def fireball(target):
        return f"Fireball hits {target}"

    def heal(target):
        return f"Heals {target}"

    def base_damage():
        return 10

    # 2. Testar o spell_combiner
    print("Testing spell combiner...")
    combined_spell = spell_combiner(fireball, heal)
    resultado1, resultado2 = combined_spell("Dragon")
    print(f"Combined spell result: {resultado1}, {resultado2}")

    # 3. Testar o power_amplifier
    print("Testing power amplifier...")
    mega_spell = power_amplifier(base_damage, 3)
    print(f"Original: {base_damage()}, Amplified: {mega_spell()}")
