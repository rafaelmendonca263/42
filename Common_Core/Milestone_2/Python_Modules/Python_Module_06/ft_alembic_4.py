import alchemy

if __name__ == "__main__":
    try:
        print("=== Alembic 4 ===")
        print("Accessing the alchemy module using 'import alchemy'")
        print(f"Testing create_air: {alchemy.create_air()}")
    except AttributeError as e:
        print("Now show that not all functions can be reached")
        print("This will raise an exception!")
        print(f"Testing the hidden create_air: {e}")

    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print(f"Testing the hidden create_earth: {alchemy.create_earth()}")
