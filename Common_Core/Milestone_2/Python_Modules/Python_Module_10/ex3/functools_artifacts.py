import operator
from functools import reduce, partial, lru_cache
from functools import singledispatch


def spell_reducer(spells: list[int], operation: str) -> int:
    ops = {"add": operator.add, "multiply": operator.mul,
           "subtraction": operator.sub,
           "division": operator.truediv, "max": max,
           "min": min, "power": operator.pow}
    if operation not in ops:
        raise ValueError(f"Invalid operation: {operation}")
    return reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    enchantments = {
        "fire_enchant": partial(base_enchantment, element="fire", power=50),
        "ice_enchant": partial(base_enchantment, element="ice", power=50),
        "lightning_enchant": partial(base_enchantment,
                                     element="lightning",
                                     power=50),
    }
    return enchantments


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    @singledispatch
    def cast_spell(spell):
        # Este é o comportamento padrão (fallback) 🛡️
        # Só é chamado se o tipo não for int, str ou list
        return f"Generic magic: {spell}"

    @cast_spell.register(int)
    def _(spell: int):
        # Tratamento para números inteiros 💥
        return f"Damage spell: {spell} power"

    @cast_spell.register(str)
    def _(spell: str):
        # Tratamento para textos ✨
        return f"Enchantment: {spell}"

    @cast_spell.register(list)
    def _(spell: list):
        # Tratamento para listas 📜
        return f"Multi-cast: {spell}"

    return cast_spell


if __name__ == "__main__":
    # 1. Testando o spell_reducer 💥
    print("Testing spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")

    # 2. Testando o memoized_fibonacci 🧠
    print("\nTesting memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")  # 55
    print(f"Fib(15): {memoized_fibonacci(15)}")  # 610

    # 3. Testando o partial_enchanter 🛠️
    print("\nTesting partial enchanter...")
    # Criamos uma função base para teste

    def base_enchant(power, element, target):
        return f"Enchanting {target} with {element} (Power: {power})"

    enchants = partial_enchanter(base_enchant)
    print(enchants["fire_enchant"](target="Sword"))
    print(enchants["ice_enchant"](target="Shield"))

    # 4. Testando o spell_dispatcher 🚦
    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(100))
    print(cast("Invisibility"))
    print(cast([10, 20, 30]))
