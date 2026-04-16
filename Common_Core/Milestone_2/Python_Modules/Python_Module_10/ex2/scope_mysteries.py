
def mage_counter() -> callable:
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> callable:
    total_power = initial_power
    
    def accumulator(spell_power: int):
        nonlocal total_power
        total_power += spell_power
        return total_power
    return accumulator


def enchantment_factory(enchantment_type: str) -> callable:
    def enchant(item: str) -> str:
        return f"{enchantment_type} {item}"
    return enchant


def memory_vault() -> dict[str, callable]:
    vault = {}

    def store_spell(spell_name: str, spell_function: callable):
        vault[spell_name] = spell_function

    def recall_spell(spell_name: str) -> callable:
        return vault.get(spell_name, "Memory not found")
    return {"store": store_spell, "recall": recall_spell}


if __name__ == "__main__":

    # Testando o mage_counter
    print("\nTesting mage counter...")
    counter = mage_counter()  # Criamos o nosso contador isolado
    print(f"Call 1: {counter()}")
    print(f"Call 2: {counter()}")
    print(f"Call 3: {counter()}")

    # Testando a enchantment_factory
    print("\nTesting enchantment factory...")
    # Criamos duas fábricas diferentes com memórias diferentes
    flaming_enchantment = enchantment_factory("Flaming")
    frozen_enchantment = enchantment_factory("Frozen")

    # Aplicamos as ferramentas aos itens
    print(flaming_enchantment("Sword"))
    print(frozen_enchantment("Shield"))
