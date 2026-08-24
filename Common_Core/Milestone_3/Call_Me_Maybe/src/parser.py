"""Module for reading, writing, and validating JSON files."""

import json
from pathlib import Path
from typing import List

from pydantic import ValidationError

from src.models import FunctionCallResult, FunctionDefinition, TestPrompt


def load_functions(file_path: str) -> List[FunctionDefinition]:
    """Load and validate function definitions from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Function definition file not found at: {file_path}",
        )

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [FunctionDefinition(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as err:
        raise ValueError(
            f"Error validating function definition file ({file_path}): {err}",
        ) from err


def load_test_prompts(file_path: str) -> List[TestPrompt]:
    """Load and validate test cases from a JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Test file not found at: {file_path}",
        )

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [TestPrompt(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as err:
        raise ValueError(
            f"Error validating test file ({file_path}): {err}",
        ) from err


def save_results(file_path: str, results: List[FunctionCallResult]) -> None:
    """Write the list of results to the output JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = [res.model_dump() for res in results]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
