"""Unit tests for the ConstrainedDecoder module."""

from unittest.mock import MagicMock
from src.decoder import ConstrainedDecoder
from src.models import FunctionDefinition


def test_fallback_parameters_add_numbers() -> None:
    """Test fallback parameter extraction for number addition."""
    mock_llm = MagicMock()
    decoder = ConstrainedDecoder(mock_llm)

    fn = FunctionDefinition(
        name="fn_add_numbers",
        description="Add two numbers together.",
        parameters={"a": {"type": "number"}, "b": {"type": "number"}},
        returns={"type": "number"}
    )

    params = decoder._fallback_parameters("What is the sum of 15 and 25?", fn)
    assert params["a"] == 15.0
    assert params["b"] == 25.0


def test_fallback_parameters_greet() -> None:
    """Test fallback parameter extraction for greeting."""
    mock_llm = MagicMock()
    decoder = ConstrainedDecoder(mock_llm)

    fn = FunctionDefinition(
        name="fn_greet",
        description="Generate a greeting.",
        parameters={"name": {"type": "string"}},
        returns={"type": "string"}
    )

    params = decoder._fallback_parameters("Greet bob", fn)
    assert params["name"] == "Bob"


def test_fallback_parameters_reverse() -> None:
    """Test fallback parameter extraction for string reversal."""
    mock_llm = MagicMock()
    decoder = ConstrainedDecoder(mock_llm)

    fn = FunctionDefinition(
        name="fn_reverse_string",
        description="Reverse a string.",
        parameters={"s": {"type": "string"}},
        returns={"type": "string"}
    )

    params = decoder._fallback_parameters("Reverse the string 'python'", fn)
    assert params["s"] == "python"
