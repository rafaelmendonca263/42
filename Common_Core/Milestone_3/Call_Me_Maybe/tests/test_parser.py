"""Unit tests for the JSON parser module."""

from pathlib import Path
from src.parser import load_functions, save_results
from src.models import FunctionCallResult


def test_load_functions(tmp_path: Path) -> None:
    """Test loading and validating function definitions."""
    d = tmp_path / "data"
    d.mkdir()
    file_path = d / "functions.json"

    file_path.write_text(
        '[{"name": "fn_add_numbers", '
        '"description": "Add two numbers", '
        '"parameters": {}, "returns": {"type": "number"}}]',
        encoding="utf-8"
    )

    functions = load_functions(str(file_path))
    assert len(functions) == 1
    assert functions[0].name == "fn_add_numbers"


def test_save_results(tmp_path: Path) -> None:
    """Test saving function call results to a JSON file."""
    d = tmp_path / "output"
    d.mkdir()
    file_path = d / "results.json"

    results = [
        FunctionCallResult(
            prompt="Test prompt",
            name="fn_add_numbers",
            parameters={"a": 1.0}
        )
    ]

    save_results(str(file_path), results)

    assert file_path.exists()
    content = file_path.read_text(encoding="utf-8")
    assert "fn_add_numbers" in content
    assert "Test prompt" in content
