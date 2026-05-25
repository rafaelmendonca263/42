import alchemy.transmutation

if __name__ == "__main__":
    try:
        print("=== Transmutation 1 ===")
        print("Import transmutation module directly")
        print(
            "Testing lead "
            "to gold:"
            f" {alchemy.transmutation.lead_to_gold()}"
        )
    except Exception as e:
        print(e)
