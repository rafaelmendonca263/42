
from abc import ABC, abstractmethod
from typing import Any, List, Union, Dict


class DataProcessor(ABC):
    def __init__(self):
        self.data_store: List[str] = []
        self.counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data_store:
            raise IndexError("No data left to output.")
        data_item = self.data_store.pop(0)
        rank = self.counter
        self.counter += 1
        return rank, data_item


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and all(
            isinstance(i, (int, float)) for i in data
        ):
            return True
        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self.data_store.append(str(item))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and all(isinstance(i, str) for i in data):
            return True
        return False

    def ingest(self, data: Union[str, List[str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        self.data_store.extend(items)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log_dict(d: Any) -> bool:
            return (
                isinstance(d, dict) and
                all(isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items())
            )

        if is_log_dict(data):
            return True
        if isinstance(data, list) and all(is_log_dict(i) for i in data):
            return True
        return False

    def ingest(
        self, data: Union[Dict[str, str], List[Dict[str, str]]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            formatted_log = ": ".join(item.values())
            self.data_store.append(formatted_log)


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Processor ===")

        print("\nTesting Numeric Processor...")
        num_proc = NumericProcessor()
        print(f"Trying to validate input '42': {num_proc.validate(42)}")
        print(f"Trying to validate input"
              f" 'Hello': {num_proc.validate('Hello')}")

        print("Test invalid ingestion "
              "of string 'foo' without prior validation:")
        try:
            num_proc.ingest("foo")
        except ValueError as e:
            print(f"Got exception: {e}")

        print("Processing data: [1, 2, 3, 4, 5]")
        num_proc.ingest([1, 2, 3, 4, 5])
        print("Extracting 3 values...")
        for i in range(3):
            rank, val = num_proc.output()
            print(f"Numeric value {rank}: {val}")

        print("\nTesting Text Processor...")
        text_proc = TextProcessor()
        print(f"Trying to validate input '42': {text_proc.validate(42)}")
        print("Processing data: ['Hello', 'Nexus', 'World']")
        text_proc.ingest(['Hello', 'Nexus', 'World'])
        print("Extracting 1 value...")
        rank, val = text_proc.output()
        print(f"Text value {rank}: {val}")

        print("\nTesting Log Processor...")
        log_proc = LogProcessor()
        print(f"Trying to validate input "
              f"'Hello': {log_proc.validate('Hello')}")
        log_data = [
            {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
        ]
        print(f"Processing data: {log_data}")
        log_proc.ingest(log_data)
        print("Extracting 2 values...")
        for i in range(2):
            rank, val = log_proc.output()
            print(f"Log entry {rank}: {val}")

    except Exception as e:
        print(e)
