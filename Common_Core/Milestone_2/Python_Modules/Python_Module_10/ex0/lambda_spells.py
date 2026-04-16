
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max_power": max(mages, key=lambda x: x["power"])["power"],
        "min_power": min(mages, key=lambda x: x["power"])["power"],
        "avg_power": round(
            sum(map(lambda x: x["power"], mages)) / len(mages),
            2
        )
    }


if __name__ == "__main__":
    # Dados de teste para os Artefatos
    test_artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'magic'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'weapon'}
    ]

    # Testando o artifact sorter
    print("\nTesting artifact sorter...")
    sorted_artifacts = artifact_sorter(test_artifacts)

    # Extraindo o primeiro e o segundo classificados para o print
    primeiro = sorted_artifacts[0]
    segundo = sorted_artifacts[1]
    print(
        f"{primeiro['name']} ({primeiro['power']} power) comes before "
        f"{segundo['name']} ({segundo['power']} power)"
    )

    # Dados de teste para os Feitiços
    test_spells = ["fireball", "heal", "shield"]

    # Testando o spell transformer
    print("\nTesting spell transformer...")
    transformed_spells = spell_transformer(test_spells)

    # O expected output mostra os feitiços separados por um espaço
    print(" ".join(transformed_spells))
