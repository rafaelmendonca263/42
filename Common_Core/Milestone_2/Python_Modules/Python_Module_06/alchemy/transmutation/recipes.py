def lead_to_gold():

    from alchemy.potions import strength_potion
    import alchemy
    import elements

    air_result = alchemy.elements.create_air()
    strength_potion_result = strength_potion()
    fire_result = elements.create_fire()

    return (
        "Recipe transmuting Lead to Gold: brew ’"
        f"{air_result}’ and ’{strength_potion_result}’ mixed "
        f"with ’{fire_result}’"
    )
