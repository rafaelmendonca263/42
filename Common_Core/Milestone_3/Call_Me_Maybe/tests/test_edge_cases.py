
import pytest
from src.parser import load_functions, load_test_prompts
from src.scorer import FunctionScorer
from src.decoder import ConstrainedDecoder
from src.models import FunctionDefinition
from unittest.mock import MagicMock


def test_load_functions_file_not_found() -> None:
    """Ensure load_functions raises FileNotFoundError for missing files."""
    with pytest.raises(FileNotFoundError):
        load_functions("non_existent_functions_file.json")


def test_load_test_prompts_file_not_found() -> None:
    """Ensure load_test_prompts raises FileNotFoundError for missing files."""
    with pytest.raises(FileNotFoundError):
        load_test_prompts("non_existent_prompts_file.json")


def test_scorer_empty_functions_list() -> None:
    """Ensure select_best_function raises ValueError
    when given an empty list."""
    mock_llm = MagicMock()
    scorer = FunctionScorer(mock_llm)
    with pytest.raises(ValueError, match="No functions available"):
        scorer.select_best_function("What is the sum?", [])


def test_decoder_fallback_edge_cases() -> None:
    """Test decoder fallback behavior with unexpected function definitions."""
    mock_llm = MagicMock()
    decoder = ConstrainedDecoder(mock_llm)

    fn = FunctionDefinition(
        name="fn_custom_unknown",
        description="A custom function",
        parameters={},
        returns={"type": "string"}
    )

    params = decoder._fallback_parameters("Do some random operation", fn)
    assert isinstance(params, dict)
