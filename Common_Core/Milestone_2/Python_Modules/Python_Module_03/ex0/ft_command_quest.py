
import sys

if __name__ == "__main__":
    try:
        print("=== Command Quest ===")

        print(f"Program name: {sys.argv[0]}")

        user_args = sys.argv[1:]

        if len(user_args) == 0:
            print("No arguments provided!")
        else:
            print(f"Arguments received: {len(user_args)}")
            for i, arg in enumerate(user_args, start=1):
                print(f"Argument {i}: {arg}")

        print(f"Total arguments: {len(sys.argv)}")
    
    except Exception as e:
        print(e)
        exit(1)