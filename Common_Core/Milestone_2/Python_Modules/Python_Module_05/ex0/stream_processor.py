
from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        try:
            total = sum(data)
            return True
            print(total)
        except TypeError:
            return False

    def process(self, data: Any) -> str:
        print(f"Processing data: {data}")

        if not self.validate(data):
            raise ValueError("Invalid numeric data")

        print("Validation: Numeric data verified")

        total = (
                int(sum(data))
                if all(isinstance(x, int) for x in data)
                else sum(data)
        )
        avg = total / len(data)

        result = (
            f"Processed {len(data)} numeric values, "
            f"sum={total}, avg={avg}"
        )
        return super().format_output(result)


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        try:
            _ = len(data)
            _ = data.split()
            return True
        except AttributeError:
            return False

    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')

        if not self.validate(data):
            raise ValueError("Invalid text data")

        print("Validation: Text data verified")

        chars = len(data)
        words = len(data.split())

        result = f"Processed text: {chars} characters, {words} words"
        return super().format_output(result)


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        try:
            level, msg = data.split(":", 1)
            return True
        except (ValueError, AttributeError):
            return False

    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')

        if not self.validate(data):
            raise ValueError("Invalid log entry")

        print("Validation: Log entry verified")

        level, message = data.split(":", 1)
        level = level.strip().upper()
        message = message.strip()

        tag = "[INFO]"
        if level == "ERROR":
            tag = "[ALERT]"
        elif level == "WARNING":
            tag = "[WARN]"

        result = f"{tag} {level} level detected: {message}"
        return super().format_output(result)


if __name__ == "__main__":

    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    try:
        print("Initializing Numeric Processor...")
        num = NumericProcessor()
        print(num.process([1, 2, 3, 4, 5]) + "\n")

        print("Initializing Text Processor...")
        txt = TextProcessor()
        print(txt.process("Hello Nexus World") + "\n")

        print("Initializing Log Processor...")
        log = LogProcessor()
        print(log.process("ERROR: Connection timeout") + "\n")

        print("=== Polymorphic Processing Demo ===")
        print("Processing multiple data types through same interface...")

        processors: List[DataProcessor] = [
            NumericProcessor(),
            TextProcessor(),
            LogProcessor()
        ]

        data_samples: List[Any] = [
            [1, 2, 3],
            "Hello World!",
            "INFO: System ready"
        ]

        for i, (proc, data) in enumerate(zip(processors, data_samples), 1):
            result = proc.process(data)
            print(f"Result {i}: {result.replace('Output: ', '')}")

        print("\nFoundation systems online. Nexus ready for advanced streams.")

    except ValueError as e:
        print(f"Validation error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
