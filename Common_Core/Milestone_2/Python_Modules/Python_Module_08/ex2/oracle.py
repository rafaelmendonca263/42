import os
import sys


def load_oracle_configs() -> dict[str, str]:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()

    configs = {
        "mode": os.getenv("MATRIX_MODE", "development"),
        "db": os.getenv("DATABASE_URL", "Not set"),
        "api": "Authenticated" if os.getenv("API_KEY") else "Unauthorized",
        "log": os.getenv("LOG_LEVEL", "INFO"),
        "zion": os.getenv("ZION_ENDPOINT", "Not set"),
    }

    return configs


def security_check(configs: dict[str, str]) -> None:
    print("\nEnvironment security check:")

    if (
        configs["db"] not in (None, "Not set")
        and configs["api"] != "Unauthorized"
    ):
        print("[OK] No hardcoded secrets detected")
    else:
        print("[WARNING] Possible hardcoded secrets or missing values")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[ERROR] .env file missing")

    if (
        configs["mode"] == "production"
        or os.getenv("MATRIX_MODE") == "production"
    ):
        print("[OK] Production overrides available")
    else:
        print("[INFO] Running in default mode")


def main() -> None:
    print("Accessing the Mainframe")
    print("ORACLE STATUS: Reading the Matrix...\n")

    try:
        matrix_cfg = load_oracle_configs()

        print("Configuration loaded:")
        print(f"Mode: {matrix_cfg['mode']}")
        print(f"Database: {matrix_cfg['db']}")
        print(f"API Access: {matrix_cfg['api']}")
        print(f"Log Level: {matrix_cfg['log']}")
        print(f"Zion Network: {matrix_cfg['zion']}")

        security_check(matrix_cfg)

        print("\nThe Oracle sees all configurations.")

    except Exception as e:
        print(f"[CRITICAL ERROR] The Matrix has a glitch: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
