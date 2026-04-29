
import sys

if __name__ == "__main__":
    print("=== Inventory System Analysis ===")

    inventory = {}
    for item in sys.argv[1:]:
        item = item.split(":")
        if item[0] not in inventory:
            if len(item) == 2:
                try:
                    inventory[item[0]] = int(item[1])
                except ValueError:
                    print(f"Quantity error for '{item[0]}': "
                          f"invalid literal for int() with base 10: '{item[1]}'")
            else:
                print(f"Error - invalid parameter '{item[0]}'")
        else:
            print(f"Redundant item '{item[0]}' - discarding")

    print(f"Got inventory: {inventory}")

    names = list(inventory)
    number_items = sum(inventory.values())
    print(f"Item list: {names}")
    print(f"Total quantity of the {len(names)} items: {number_items}")

    for item in inventory:
        percentage = (inventory[item] / number_items) * 100
        print(f"Item {item} represents ({percentage:.1f}%)")

    most_abundant = max(inventory.values())
    most_abundant_name = max(inventory, key=inventory.get)
    least_abundant = min(inventory.values())
    least_abundant_name = min(inventory, key=inventory.get)

    print(
        f"Item most abundant: {most_abundant_name} "
        f"with a quantity {most_abundant}"
    )

    print(
        f"Item least abundant: {least_abundant_name} "
        f"with a quantity {least_abundant}"
    )

    new_item = "magic_item: 1"
    new_item = new_item.split('"')
    new_item = new_item[0].split(":")

    inventory[new_item[0]] = int(new_item[1])

    print(f"Updated inventory: {inventory}")
