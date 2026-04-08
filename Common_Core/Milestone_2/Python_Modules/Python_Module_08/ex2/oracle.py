
"""
oracle.py - Access the Mainframe
Loads configuration from environment variables or .env file,
validates settings, and prints Oracle status.
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("Accessing the Mainframe")
print("ORACLE STATUS: Reading the Matrix...\n")

CONFIG_VARS = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": None,
    "API_KEY": None,
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": None
}

for key in CONFIG_VARS:
    CONFIG_VARS[key] = os.getenv(key, CONFIG_VARS[key])


def check_hardcoded_secrets(config):
    """Detecta valores padrão ou hardcoded"""
    hardcoded = []
    for key, value in config.items():
        if value in (None, "", "password", "user", "secret"):
            hardcoded.append(key)
    return hardcoded


if __name__ == "__main__":
    print("Configuration loaded:")
    print(f"Mode: {CONFIG_VARS['MATRIX_MODE']}")
    print(f"Database: {CONFIG_VARS['DATABASE_URL'] or 'Not set'}")
    print(f"API Access: "
          f"{'Authenticated' if CONFIG_VARS['API_KEY'] else 'Not set'}")
    print(f"Log Level: {CONFIG_VARS['LOG_LEVEL']}")
    print(f"Zion Network: {CONFIG_VARS['ZION_ENDPOINT'] or 'Not set'}\n")

    print("Environment security check:")

    hardcoded = check_hardcoded_secrets(CONFIG_VARS)
    if hardcoded:
        print(f"[ERROR] Hardcoded secrets found: {', '.join(hardcoded)}")
    else:
        print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file missing!")

    if CONFIG_VARS['MATRIX_MODE'] == "production":
        required_keys = ("DATABASE_URL", "API_KEY")
        missing = [
            k for k in required_keys
            if not CONFIG_VARS[k]
        ]
    if missing:
        print(f"[ERROR] Missing production secrets: {', '.join(missing)}")
    else:
        print("[INFO] No production overrides set")

    print("\nThe Oracle sees all configurations.")
