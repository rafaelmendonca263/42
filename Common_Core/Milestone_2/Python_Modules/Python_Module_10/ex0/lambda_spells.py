from collections import abc


def artifact_sorter(
    artifacts: list[dict[str, int | str]],
) -> list[dict[str, int | str]]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(
    mages: list[dict[str, int | str]], min_power: int
) -> list[dict[str, int | str]]:
    return list(
        filter(
            lambda x: isinstance(x["power"], (int, float))
            and x["power"] >= min_power,
            mages,
        )
    )


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict[str, int | str]]) -> dict[str, int | float]:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    powers: list[int | float] = [
        m["power"] for m in mages if isinstance(m["power"], (int, float))
    ]

    if not powers:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    get_max: abc.Callable[[list[int | float]], int | float] = lambda x: max(x)
    get_min: abc.Callable[[list[int | float]], int | float] = lambda x: min(x)
    get_avg: abc.Callable[[list[int | float]], float] = lambda x: round(
        sum(x) / len(x), 2
    )

    return {
        "max_power": int(get_max(powers)),
        "min_power": int(get_min(powers)),
        "avg_power": get_avg(powers),
    }


def main() -> None:
    print("Testing artifact sorter...")
    artifacts: list[dict[str, int | str]] = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} power)"
        " comes before "
        f"{sorted_artifacts[1]['name']} ({sorted_artifacts[1]['power']} power)"
    )

    print("\nTesting spell transformer...")
    spells: list[str] = ["fireball", "heal shield"]
    transformed = spell_transformer(spells)
    for spell in transformed:
        print(spell)


if __name__ == "__main__":
    main()
