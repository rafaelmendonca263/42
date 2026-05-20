import alchemy

if __name__ == "__main__":
    try:
        print("=== Distillation 1 ===")
        print("Using: 'import alchemy' structure to access potions")
        print(f"Testing strength_potion: {alchemy.strength_potion()}")
        print(f"Testing heal alias:: {alchemy.heal()}")
    except Exception as e:
        print(e)
