
import alchemy
import alchemy.elements

if "__main__" == __name__:
    print("\n=== Sacred Scroll Mastery ===\n")
    print("Testing direct module access:")

    try:
        print("alchemy.elements.create_fire(): "
              f"{alchemy.elements.create_fire()}")
    except AttributeError as e:
        print(f"alchemy.elements.create_fire(): "
              f"{e} - not exposed")

    try:
        print("alchemy.elements.create_water(): "
              "{alchemy.elements.create_water()}")
    except AttributeError as e:
        print(f"alchemy.elements.create_water(): "
              f"{e} - not exposed")

    try:
        print("alchemy.elements.create_earth(): "
              f"{alchemy.elements.create_earth()}")
    except AttributeError as e:
        print(f"alchemy.elements.create_earth(): "
              f"{e} - not exposed")

    try:
        print("alchemy.elements.create_air(): "
              f"{alchemy.elements.create_air()}")
    except AttributeError as e:
        print(f"alchemy.elements.create_air(): {e} - not exposed")

    print("\nTesting package-level access (controlled by __init__.py):")

    try:
        print(f"alchemy.create_fire(): "
              f"{alchemy.create_fire()}")
    except AttributeError as e:
        print(f"alchemy.create_fire(): "
              f"{e} - not exposed")

    try:
        print("alchemy.create_water(): "
              f"{alchemy.create_water()}")
    except AttributeError as e:
        print("alchemy.create_water(): "
              f"{e} - not exposed")

    try:
        print("alchemy.create_earth(): "
              f"{alchemy.create_earth()}")
    except AttributeError as e:
        print(f"alchemy.create_earth(): "
              f"{e} - not exposed")

    try:
        print(f"alchemy.create_air(): "
              f"{alchemy.create_air()}")
    except AttributeError as e:
        print(f"alchemy.create_air(): {e} "
              "- not exposed")

    print("\nPackage metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")
