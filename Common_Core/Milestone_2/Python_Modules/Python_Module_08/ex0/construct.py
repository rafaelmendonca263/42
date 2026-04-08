
import sys
import os
import site


def main():
    if sys.prefix != sys.base_prefix:
        print("MATRIX STATUS: Welcome to the construct")
        print("Current Python:", sys.executable)
        print("Virtual Environment:", os.path.basename(sys.prefix))
        print("Environment Path:", sys.prefix)
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print("Package installation path:")
        print(site.getsitepackages()[0])
    else:
        print("MATRIX STATUS: You're still plugged in")
        print("Current Python:", sys.executable)
        print("Virtual Environment: None detected")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows")
        print("Then run this program again.")


if __name__ == "__main__":
    main()
