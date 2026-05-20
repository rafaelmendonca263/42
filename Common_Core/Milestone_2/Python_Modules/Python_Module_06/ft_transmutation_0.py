import alchemy.transmutation.recipes

if __name__ == "__main__":
    try:
        print("=== Transmutation 0 ===")
        print("Using file alchemy/transmutation/recipes.py directly")
        print(
            "Testing lead "
            f"to gold: {alchemy.transmutation.recipes.lead_to_gold()}"
        )
    except Exception as e:
        print(e)
