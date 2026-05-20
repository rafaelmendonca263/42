from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(artifacts, key=lambda x: x.get("power", 0), reverse=True)


def power_filter(mages: list[dict[str, Any]],
                 min_power: int) -> list[dict[str, Any]]:
    return list(filter(lambda m: m.get("power", 0) >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, int | float]:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    powers = list(map(lambda m: m.get("power", 0), mages))

    max_power = max(powers, key=lambda p: p)
    min_power = min(powers, key=lambda p: p)
    avg_power = round(sum(powers) / len(powers), 2)

    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power,
    }


if __name__ == "__main__":
    print("Testing artifact sorter...")
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "Focus"},
        {"name": "Fire Staff", "power": 92, "type": "Weapon"},
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    print(f"{sorted_artifacts[0]['name']} "
          f"({sorted_artifacts[0]['power']} power) "
          f"comes before {sorted_artifacts[1]['name']} "
          f"({sorted_artifacts[1]['power']} power)")

    print("\nTesting spell transformer...")
    spells = ["fireball", "heal", "shield"]
    print(" ".join(spell_transformer(spells)))
