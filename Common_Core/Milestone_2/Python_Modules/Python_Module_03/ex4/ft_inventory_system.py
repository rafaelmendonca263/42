
if __name__ == "__main__":
    print("=== Inventory System Analysis ===")

    inventory = {
        "sword":   {"quantity": 1, "type": "weapon", "value": 100},
        "potion":  {"quantity": 5, "type": "consumable", "value": 10},
        "shield":  {"quantity": 2, "type": "armor", "value": 50},
        "armor":   {"quantity": 3, "type": "armor", "value": 150},
        "helmet":  {"quantity": 1, "type": "armor", "value": 70}
    }

    total_items = sum(item["quantity"] for item in inventory.values())
    unique_items = len(inventory)
    print(f"Total items in inventory: {total_items}")
    print(f"Unique item types: {unique_items}")

    print("\n=== Current Inventory ===")
    sorted_items = sorted(
        inventory.items(),
        key=lambda x: x[1]["quantity"],
        reverse=True
    )
    for item, data in sorted_items:
        percentage = (data["quantity"] / total_items) * 100
        print(f"{item}: {data['quantity']} units ({percentage:.1f}%)")

    print("\n=== Inventory Statistics ===")
    most_abundant = sorted_items[0]
    least_abundant = sorted_items[-1]
    print(f"Most abundant: {most_abundant[0]} ({most_abundant[1]['quantity']} units)")
    print(f"Least abundant: {least_abundant[0]} ({least_abundant[1]['quantity']} units)")

    print("\n=== Item Categories ===")
    categories = {"Moderate": {}, "Scarce": {}}
    for item, data in inventory.items():
        if data["quantity"] >= 5:
            categories["Moderate"][item] = data["quantity"]
        else:
            categories["Scarce"][item] = data["quantity"]
    print(f"Moderate: {categories['Moderate']}")
    print(f"Scarce: {categories['Scarce']}")

    print("\n=== Management Suggestions ===")
    restock = [item for item, data in inventory.items() if data["quantity"] <= 1]
    print(f"Restock needed: {restock}")

    print("\n=== Dictionary Properties Demo ===")
    print(f"Dictionary keys: {list(inventory.keys())}")
    print(f"Dictionary values: {[data['quantity'] for data in inventory.values()]}")
    print("Sample lookup - 'sword' in inventory:", "sword" in inventory)