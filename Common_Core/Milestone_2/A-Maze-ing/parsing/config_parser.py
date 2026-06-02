from typing import cast, TYPE_CHECKING, Optional
from types import FrameType
import signal
import sys


if TYPE_CHECKING:
    from mazegen.mazegen import MazeConfig


def handle_signal(sig: int, frame: Optional[FrameType]) -> None:
    if sig == signal.SIGINT:
        print("\nCtrl+C detected — User kill the program.")
        sys.exit(1)
    frame = frame
    if sig == signal.SIGTSTP:
        print("\nCtrl+Z detected — No permission to exit of the program.")


class ConfigParser:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def clean_line(self, line: str) -> str | None:
        if line.strip() == "":
            return None
        line = line.strip()
        if "#" in line:
            if line.startswith("#") or line == "":
                return None
            line = line.split("#", 1)[0].strip()
        return line

    def split_key_value(self, line: str) -> tuple[str, str]:
        if "=" not in line:
            raise ValueError("Invalid configuration format. "
                             "Expected 'KEY=VALUE'.")
        key, value = line.split("=", 1)
        return key.strip(), value.strip()

    def load_config(self) -> dict[str, str] | None:
        try:
            with open(self.config_file, "r") as file:
                config = {}
                for line in file:
                    cleaned_line = self.clean_line(line)
                    if cleaned_line is None:
                        continue

                    key, value = self.split_key_value(cleaned_line)

                    if key in config:
                        raise ValueError(f"Duplicate key: {key}")

                    config[key] = value

                return config
        except PermissionError:
            print("Error: The file hasn't permission!")
            print("For executes the program enter: chmod +r config.txt")
            return None
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except Exception as e:
            print(f"Error reading config: {e}")
            return None

    def validate_config(
        self,
        config: dict[str, str]
    ) -> "MazeConfig":

        validated: dict[str, int | tuple[int, int] | str | bool] = {}

        for key, value in config.items():
            if key in ["WIDTH", "HEIGHT", "SEED"]:
                if not value.isdigit() or int(value) <= 0:
                    raise ValueError(f"{key} must be a positive integer")
                num: int = int(value)
                if key == "WIDTH":
                    if num > 42:
                        raise ValueError("WIDTH must be less "
                                         "than or equal to 42")
                    if num < 9:
                        raise ValueError("WIDTH must be greater "
                                         "than or equal to 8")
                elif key == "HEIGHT":
                    if num < 8:
                        raise ValueError("HEIGHT must be greater "
                                         "than or equal to 9")
                    if num > 42:
                        raise ValueError("HEIGHT must be "
                                         "less than or equal to 42")
                elif key == "SEED":
                    try:
                        if config["SEED"] is not None:
                            int(config["SEED"])
                        else:
                            validated[key] = None
                    except ValueError as e:
                        print(f"{e}")
                validated[key] = num

            elif key in ["ENTRY", "EXIT"]:
                parts: list[str] = value.split(",")
                if (
                    len(parts) != 2
                    or not all(p.strip().isdigit() for p in parts)
                ):
                    raise ValueError(f"{key} must be in "
                                     "format x,y with integers")
                x: int = int(parts[0].strip())
                y: int = int(parts[1].strip())
                if x < 0 or y < 0:
                    raise ValueError(f"{key} must be non-negative")
                validated[key] = (x, y)

            elif key == "OUTPUT_FILE":
                if not value.endswith(".txt"):
                    raise ValueError("OUTPUT_FILE must end with .txt")
                validated[key] = value

            elif key == "PERFECT":
                if value not in ["True", "False"]:
                    raise ValueError("PERFECT must be True or False")
                validated[key] = value == "True"

        required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT" ]
        for key in required:
            if key not in validated:
                raise KeyError(f"Missing required key: {key}")

        return cast("MazeConfig", validated)

    def parser_entry_exit(self, config: "MazeConfig") -> bool:
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        width = config["WIDTH"]
        height = config["HEIGHT"]

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("ENTRY coordinates must "
                             "be within maze dimensions")

        if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
            raise ValueError("EXIT coordinates must be within maze dimensions")

        return True

    def parse(self) -> "MazeConfig":
        config = self.load_config()
        if config is None:
            exit(1)

        try:
            validated_config = self.validate_config(config)

            if validated_config["ENTRY"] == validated_config["EXIT"]:
                print("Error: ENTRY and EXIT cannot be equal!")
                exit(1)

            self.parser_entry_exit(validated_config)
            return validated_config

        except (KeyError, ValueError) as e:
            print(f"Configuration validation error: {e}")
            exit(1)


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTSTP, handle_signal)
