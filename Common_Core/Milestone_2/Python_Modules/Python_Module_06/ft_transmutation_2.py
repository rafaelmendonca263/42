import alchemy

if __name__ == "__main__":
    try:
        print("=== Transmutation 2 ===")
        print("Import alchemy module only")
        print("Testing lead " f"to gold: {alchemy.lead_to_gold()}")
    except Exception as e:
        print(e)
