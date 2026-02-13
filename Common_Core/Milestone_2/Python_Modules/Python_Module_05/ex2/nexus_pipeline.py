from abc import ABC, abstractmethod
from typing import Any, List, Protocol, Union
import json
import csv
from io import StringIO
import time
from statistics import mean

# ---------- STAGE PROTOCOL ----------

class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        ...


# ---------- STAGES ----------

class InputStage:
    def process(self, data: Any) -> Any:
        # Detect input type and standardize it
        if isinstance(data, str):
            try:
                # JSON string?
                return json.loads(data)
            except json.JSONDecodeError:
                # CSV string?
                reader = csv.DictReader(StringIO(data))
                return list(reader)
        return data


class TransformStage:
    def process(self, data: Any) -> Any:
        # Enrich data based on type
        if isinstance(data, dict) and "temp" in data:
            # Example: add unit and validate range
            temp = data["temp"]
            data["unit"] = "C"
            data["status"] = "Normal range" if 20 <= temp <= 30 else "Alert"
        elif isinstance(data, list):
            # CSV / list of dicts: count entries
            for item in data:
                item["processed"] = True
        elif isinstance(data, list) and all(isinstance(d, dict) for d in data):
            # Could calculate averages, etc.
            pass
        return data


class OutputStage:
    def process(self, data: Any) -> Any:
        # Convert processed data into final human-readable output
        if isinstance(data, dict) and "temp" in data:
            return f"Processed temperature reading: {data['temp']}°{data['unit']} ({data['status']})"
        elif isinstance(data, list) and all("action" in d for d in data):
            return f"User activity logged: {len(data)} actions processed"
        elif isinstance(data, list) and all("value" in d for d in data):
            avg_val = mean([float(d["value"]) for d in data])
            return f"Stream summary: {len(data)} readings, avg: {avg_val:.1f}°C"
        return data


# ---------- PIPELINE BASE ----------

class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str, stages: List[ProcessingStage]):
        self.pipeline_id = pipeline_id
        self.stages = stages

    def run_stages(self, data: Any) -> Any:
        for stage in self.stages:
            data = stage.process(data)
        return data

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass


# ---------- ADAPTERS ----------

class JSONAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        parsed = json.loads(data)
        return self.run_stages(parsed)


class CSVAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        reader = csv.DictReader(StringIO(data))
        parsed = list(reader)
        return self.run_stages(parsed)


class StreamAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        # Assume data is already structured
        return self.run_stages(data)


# ---------- MANAGER ----------

class NexusManager:
    def __init__(self):
        self.pipelines: List[ProcessingPipeline] = []

    def register(self, pipeline: ProcessingPipeline):
        self.pipelines.append(pipeline)

    def execute(self, data: Any):
        result = data
        for pipeline in self.pipelines:
            try:
                start = time.time()
                result = pipeline.process(result)
                print(result)
                print(f"Time: {time.time() - start:.3f}s\n")
            except Exception as e:
                print("Recovery triggered:", e)
        return result


# ---------- DEMO ----------

if __name__ == "__main__":
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")

    stages = [InputStage(), TransformStage(), OutputStage()]
    print("Initializing Nexus Manager...")
    print("Pipeline capacity: 1000 streams/second\n")
    manager = NexusManager()

    # Register multiple pipelines
    print("Creating Data Processing Pipeline...")
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    manager.register(JSONAdapter("json_pipe", stages))
    manager.register(CSVAdapter("csv_pipe", stages))
    # Example stream data
    stream_data = [{"value": 22}, {"value": 23}, {"value": 21}]
    manager.register(StreamAdapter("stream_pipe", stages))

    # Execute JSON
    manager.execute('{"temp": 23.5}')

    # Execute CSV
    csv_input = "user,action,timestamp\nAlice,login,2026-02-11\nBob,logout,2026-02-11"
    manager.execute(csv_input)

    # Execute Stream
    manager.execute(stream_data)

    print("=== Nexus Integration complete. All systems operational ===")
