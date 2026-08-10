import json
from pathlib import Path
from typing import Dict, List, Union
from src.models import TestInput, FunctionDefinition


def load_test_inputs(file_path: Union[str, Path]) -> List[TestInput]:
    """Load and validate test inputs from the JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    res = []
    for item in raw_data:
        res.append(TestInput(**item))
    return res


def load_function_definitions(file_path: Union[str, Path]) -> Dict[str, FunctionDefinition]:
    """Load and validate function definitions from the JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    res = {}
    for name, details in raw_data.items():
        res[name] = FunctionDefinition(**details)

    return res
