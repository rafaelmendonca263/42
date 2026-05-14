
import importlib


dependencies = ["pandas", "numpy", "matplotlib"]
modules = {}

print("LOADING STATUS: Loading programs...")
print("Checking dependencies:")


for dep in dependencies:
    try:
        if dep == "matplotlib":
            modules["matplotlib_pkg"] = importlib.import_module("matplotlib")
            modules[dep] = importlib.import_module("matplotlib.pyplot")
            version = modules["matplotlib_pkg"].__version__
        else:
            modules[dep] = importlib.import_module(dep)
            version = modules[dep].__version__
        print(f"[OK] {dep} ({version})")
    except ModuleNotFoundError:
        print(f"[ERROR] {dep} not found")
        exit(1)


if len(modules) < len(dependencies) + 1:
    print("Missing dependencies detected.")
    print("Install with:")
    print("pip install -r requirements.txt")
    print("or")
    print("poetry install")
    exit(1)

pd = modules["pandas"]
np = modules["numpy"]
plt = modules["matplotlib"]


def main() -> None:
    print("Analyzing Matrix data...")
    data = np.random.rand(1000, 2)
    x = data[:, 0]
    y = data[:, 1]

    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, c="blue", alpha=0.5)
    plt.title("Matrix Data Analysis")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.grid(True)
    output_file = "matrix_analysis.png"
    plt.savefig(output_file)
    plt.close()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
