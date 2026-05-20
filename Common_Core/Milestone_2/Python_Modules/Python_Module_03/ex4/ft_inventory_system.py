import sys
from typing import Dict, List

if __name__ == "__main__":
    try:
        print("=== Inventory System Analysis ===")

        if len(sys.argv) <= 1:
            print("Usage: python3 ft_inventory_system.py <object>:<int> ... ")

        inventory: Dict[str, int] = {}
        for arg in sys.argv[1:]:
            parts: List[str] = arg.split(":")
            if parts[0] not in inventory:
                if len(parts) == 2:
                    try:
                        inventory[parts[0]] = int(parts[1])
                    except ValueError as e:
                        print(f"Quantity error for '{parts[0]}': {e}")
                else:
                    print(f"Error - invalid parameter '{parts[0]}'")
            else:
                print(f"Redundant parts '{parts[0]}' - discarding")

        if not inventory:
            exit(1)

        print(f"Got inventory: {inventory}")

        names = list(inventory)
        number_items = sum(inventory.values())
        print(f"Item list: {names}")

        for item in inventory:
            try:
                percentage = (inventory[item] / number_items) * 100
                print(
                    f"Total quantity of the {len(names)} "
                    f"items: {number_items}"
                )
            except ZeroDivisionError:
                print("Error: All items need to be at leat one in quantity")
                exit(1)
            print(f"Item {item} represents ({percentage:.1f}%)")

        most_abundant = max(inventory.values())
        most_abundant_name = max(inventory, key=lambda k: inventory[k])
        least_abundant = min(inventory.values())
        least_abundant_name = min(inventory, key=lambda k: inventory[k])

        print(
            f"Item most abundant: {most_abundant_name} "
            f"with a quantity {most_abundant}"
        )

        print(
            f"Item least abundant: {least_abundant_name} "
            f"with a quantity {least_abundant}"
        )

        raw_new_item: str = "magic_item: 1"
        split_item: List[str] = raw_new_item.split(":")

        inventory[split_item[0].strip()] = int(split_item[1])

        print(f"Updated inventory: {inventory}")

    except Exception as e:
        print(e)
        exit(1)
