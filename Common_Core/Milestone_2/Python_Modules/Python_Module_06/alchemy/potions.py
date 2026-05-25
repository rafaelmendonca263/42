def healing_potion() -> str:
    from alchemy.elements import create_earth, create_air

    earth_result = create_earth()
    air_result = create_air()

    return f"Healing potion brewed with {earth_result} and {air_result}"


def strength_potion() -> str:
    from elements import create_water, create_fire

    water_result = create_water()
    fire_result = create_fire()

    return f"Streagth potion brewed with {fire_result} and {water_result}"
