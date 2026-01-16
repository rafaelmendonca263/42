
def ft_seed_inventory(name,number,unit):
    seed_name = name.capitalize()
    if unit == "packets":
        print(f"{seed_name} seeds: {number} packets available")
    elif unit == "grams":
        print(f"{seed_name} seeds: {number} grams total")
    elif unit == "area":
        print(f"{seed_name} seeds: covers {number} square meters")
    else:
         print(f"{seed_name} seeds: {number} {unit}")