from abc import ABC, abstractmethod
from typing import Any, List, Union, Dict


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data_store: List[tuple[int, str]] = []
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
        return self.data_store.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and all(
            isinstance(i, (int, float)) for i in data
        ):
            return True
        return False

    def ingest(self, data: Union[int, float, List[Union[int, float]]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self.data_store.append((self.counter, str(item)))
            self.counter += 1


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
        for item in items:
            self.data_store.append((self.counter, item))
            self.counter += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log_dict(d: Any) -> bool:
            return (
                isinstance(d, dict)
                and "log_level" in d
                and "log_message" in d
                and isinstance(d["log_level"], str)
                and isinstance(d["log_message"], str)
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
            formatted_log = f"{item['log_level']}: {item['log_message']}"
            self.data_store.append((self.counter, formatted_log))
            self.counter += 1


class DataStream:
    def __init__(self) -> None:
        self.processors: List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            found = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    found = True
                    break
            if not found:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for p in self.processors:
            name = p.__class__.__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {p.counter} items processed, "
                f"remaining {len(p.data_store)} on processor"
            )


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Stream ===\n")
        print("Initialize Data Stream...")
        ds = DataStream()
        ds.print_processors_stats()

        print("\nRegistering Numeric Processor\n")
        num_p = NumericProcessor()
        ds.register_processor(num_p)

        batch = [
            "Hello world",
            [3.14, -1, 2.71],
            [
                {
                    "log_level": "WARNING",
                    "log_message": "Telnet access! Use ssh instead",
                },
                {"log_level": "INFO", "log_message": "User wil is connected"},
            ],
            42,
            ["Hi", "five"],
        ]

        print(f"Send first batch of data on stream: {batch}")
        ds.process_stream(batch)
        ds.print_processors_stats()

        print("\nRegistering other data processors")
        txt_p, log_p = TextProcessor(), LogProcessor()
        ds.register_processor(txt_p)
        ds.register_processor(log_p)

        print("Send the same batch again")
        ds.process_stream(batch)
        ds.print_processors_stats()

        print(
            "\nConsume some elements from the data processors: "
            "Numeric 3, Text 2, Log 1"
        )
        for _ in range(3):
            num_p.output()

        for _ in range(2):
            txt_p.output()
        log_p.output()
        ds.print_processors_stats()

    except Exception as e:
        print(e)
