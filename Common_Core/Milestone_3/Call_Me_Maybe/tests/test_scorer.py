"""Unit tests for the FunctionScorer module."""

from unittest.mock import MagicMock
from src.scorer import FunctionScorer
from src.models import FunctionDefinition, FunctionParameterSchema


def test_function_scorer_initialization() -> None:
    """Test that FunctionScorer initializes correctly with a mock LLM."""
    mock_llm = MagicMock()
    scorer = FunctionScorer(mock_llm)
    assert scorer.llm == mock_llm


def test_select_best_function_keyword_fallback() -> None:
    """Test that intent matching correctly routes standard commands."""
    mock_llm = MagicMock()
    scorer = FunctionScorer(mock_llm)

    functions = [
        FunctionDefinition(
            name="fn_add_numbers",
            description="Add numbers",
            parameters={
                "a": FunctionParameterSchema(type="number"),
                "b": FunctionParameterSchema(type="number")
            },
            returns={"type": "number"}
        ),
        FunctionDefinition(
            name="fn_greet",
            description="Greet user",
            parameters={
                "name": FunctionParameterSchema(type="string")
            },
            returns={"type": "string"}
        )
    ]

    selected = (
        scorer.select_best_function("What is the sum of 10 and 20?", functions)
    )
    assert selected.name == "fn_add_numbers"

    selected_greet = scorer.select_best_function("Greet alice", functions)
    assert selected_greet.name == "fn_greet"
