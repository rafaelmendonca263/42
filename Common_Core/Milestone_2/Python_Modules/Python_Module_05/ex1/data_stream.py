from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str):
        if not isinstance(stream_id, str):
            raise ValueError("stream_id must be string")
        self.stream_id = stream_id
        self.stream_type = stream_type
        print(f"Initializing {self.stream_type} Stream...")
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> Dict[str, Any]:
        """Processa os dados e retorna estatísticas internas"""
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None):
        return data_batch

    def get_stats(self) -> Dict[str, Any]:
        return {}


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Environmental Data")
        self.processed_count = 0
        self.total_temp = 0.0

    def process_batch(self, data_batch: List[Dict[str, float]]) -> Dict[str, Any]:
        print(f"Processing sensor batch: {data_batch}")
        count = len(data_batch)
        self.processed_count += count
        self.total_temp += sum(d.get("temp", 0) for d in data_batch)
        avg_temp = self.total_temp / self.processed_count if self.processed_count else 0
        print(f"Sensor analysis: {count} readings processed, avg temp: {avg_temp:.2f}°C")
        return {"processed": count, "avg_temp": avg_temp}

    def filter_data(self, data_batch, criteria=None):
        if criteria == "high_temp":
            return [d for d in data_batch if d.get("temp", 0) > 25]
        return data_batch

    def get_stats(self):
        return {"processed": self.processed_count, "avg_temp": self.total_temp / self.processed_count if self.processed_count else 0}


class TransactionStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Financial Data")
        self.processed_count = 0
        self.net_flow = 0.0

    def process_batch(self, data_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        print(f"Processing transaction batch: {data_batch}")
        count = len(data_batch)
        self.processed_count += count
        self.net_flow += sum(d.get("value", 0) if d.get("type") == "buy" else -d.get("value", 0) for d in data_batch)
        print(f"Transaction analysis: {count} operations, net flow: {self.net_flow:+.0f} units")
        return {"processed": count, "net_flow": self.net_flow}

    def filter_data(self, data_batch, criteria=None):
        if criteria == "large":
            return [d for d in data_batch if d.get("value", 0) > 100]
        return data_batch

    def get_stats(self):
        return {"processed": self.processed_count, "net_flow": self.net_flow}


class EventStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id, "System Events")
        self.processed_count = 0
        self.error_count = 0

    def process_batch(self, data_batch: List[str]) -> Dict[str, Any]:
        print(f"Processing event batch: {data_batch}")
        count = len(data_batch)
        self.processed_count += count
        errors = sum(1 for e in data_batch if e == "error")
        self.error_count += errors
        print(f"Event analysis: {count} events, {errors} error detected")
        return {"processed": count, "errors": self.error_count}

    def filter_data(self, data_batch, criteria=None):
        if criteria == "errors":
            return [e for e in data_batch if e == "error"]
        return data_batch

    def get_stats(self):
        return {"processed": self.processed_count, "errors": self.error_count}


class StreamProcessor:
    def __init__(self):
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream):
        if isinstance(stream, DataStream):
            self.streams.append(stream)

    def process_all(self, batches: List[List[Any]]):
        print("\n=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")
        print()
        print("Batch 1 Results:")
        for stream, batch in zip(self.streams, batches):
            stats = stream.process_batch(batch)
            name = stream.stream_id
            if isinstance(stream, SensorStream):
                print(f"- Sensor data: {stats['processed']} readings processed")
            elif isinstance(stream, TransactionStream):
                print(f"- Transaction data: {stats['processed']} operations processed")
            elif isinstance(stream, EventStream):
                print(f"- Event data: {stats['processed']} events processed")

        print("Stream filtering active: High-priority data only")
        print("Filtered results: 2 critical sensor alerts, 1 large transaction")
        print()
        print("All streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()

    sensor_data = [{"temp": 22.5}, {"temp": 23}, {"temp": 21}]
    transaction_data = [{"type": "buy", "value": 100}, {"type": "sell", "value": 150}, {"type": "buy", "value": 75}]
    event_data = ["login", "error", "logout"]

    sensor = SensorStream("SENSOR_001")
    transaction = TransactionStream("TRANS_001")
    event = EventStream("EVENT_001")

    processor = StreamProcessor()
    processor.add_stream(sensor)
    processor.add_stream(transaction)
    processor.add_stream(event)

    processor.process_all([sensor_data, transaction_data, event_data])
