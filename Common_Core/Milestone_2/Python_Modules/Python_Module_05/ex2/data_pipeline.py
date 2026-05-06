from abc import ABC, abstractmethod
from typing import Any, List, Protocol, Tuple


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.data_store: List[str] = []
        self.total_count: int = 0
        self.rank_counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> Tuple[int, str]:
        if not self.data_store:
            raise IndexError("No data left to output.")
        item = self.data_store.pop(0)
        rank = self.rank_counter
        self.rank_counter += 1
        return rank, item


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        return isinstance(data, list) and all(
            isinstance(i, (int, float)) for i in data
        )

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self.data_store.append(str(item))
            self.total_count += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return isinstance(data, list) and all(
            isinstance(i, str) for i in data
        )

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self.data_store.append(item)
            self.total_count += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log(d: Any) -> bool:
            return isinstance(d, dict) and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in d.items()
            )
        if is_log(data):
            return True
        return isinstance(data, list) and all(is_log(i) for i in data)

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            msg = ": ".join(item.values())
            self.data_store.append(msg)
            self.total_count += 1


class ExportPlugin(Protocol):
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(item[1] for item in data))


class JSONExportPlugin:
    def process_output(self, data: List[Tuple[int, str]]) -> None:
        print("JSON Output:")
        json_items = [f'"item_{idx}": "{val}"' for idx, val in data]
        print("{" + ", ".join(json_items) + "}")


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
                print(f"DataStream error - No processor for: {element}")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            collected = []
            for _ in range(nb):
                if proc.data_store:
                    collected.append(proc.output())
            if collected:
                plugin.process_output(collected)

    def print_processors_stats(self) -> None:
        print("\n== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for p in self.processors:
            name = p.__class__.__name__.replace("Processor", " Processor")
            print(f"{name}: total {p.total_count} items processed, "
                  f"remaining {len(p.data_store)} on processor")


if __name__ == "__main__":
    try:
        print("=== Code Nexus - Data Pipeline ===\n")
        ds = DataStream()
        ds.print_processors_stats()

        print("Registering Processors")
        num_p, txt_p, log_p = NumericProcessor(), TextProcessor(), LogProcessor()
        for p in [num_p, txt_p, log_p]:
            ds.register_processor(p)

        batch1 = [
            'Hello world', [3.14, -1, 2.71],
            [{'log_level': 'WARNING',
              'log_message': 'Telnet access! Use ssh instead'},
             {'log_level': 'INFO',
              'log_message': 'User wil is connected'}],
            42, ['Hi', 'five']
        ]

        print(f"Send first batch of data on stream: {batch1}")
        ds.process_stream(batch1)
        ds.print_processors_stats()

        print("Send 3 processed data from each processor to a CSV plugin:")
        ds.output_pipeline(3, CSVExportPlugin())
        ds.print_processors_stats()

        batch2 = [
            21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
            [{'log_level': 'ERROR', 'log_message': '500 server crash'},
             {'log_level': 'NOTICE', 'log_message': 'Certificate expires'}],
            [32, 42, 64, 84, 128, 168], 'World hello'
        ]

        print(f"Send another batch of data: {batch2}")
        ds.process_stream(batch2)
        ds.print_processors_stats()

        print("Send 5 processed data from each processor to a JSON plugin:")
        ds.output_pipeline(5, JSONExportPlugin())
        ds.print_processors_stats()

    except Exception as e:
        print(e)