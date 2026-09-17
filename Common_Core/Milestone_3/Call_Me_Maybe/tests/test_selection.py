from typing import Any
import pytest
from src.models import FunctionDefinition, FunctionParameterSchema
from src.constrained_decoder import ConstrainedJSONDecoder
from src.structure import VocabularyManager
from llm_sdk import Small_LLM_Model  # type: ignore


@pytest.fixture
def mock_setup() -> tuple[Any, VocabularyManager]:
    llm = Small_LLM_Model()
    vocab_path = llm.get_path_to_vocab_file()
    vocab_manager = VocabularyManager(vocab_path)
    return llm, vocab_manager


def test_1_add_numbers_small(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_add_numbers",
        description="Add two numbers",
        parameters={
            "a": FunctionParameterSchema(type="number"),
            "b": FunctionParameterSchema(type="number")
        }
    )
    result = decoder.extract_parameters("What is the sum of 2 and 3?", fn_def)
    assert result.get("a") == 2
    assert result.get("b") == 3


def test_2_add_numbers_large(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_add_numbers",
        description="Add two numbers",
        parameters={
            "a": FunctionParameterSchema(type="number"),
            "b": FunctionParameterSchema(type="number")
        }
    )
    result = decoder.extract_parameters("What is the sum of 265 and 345?",
                                        fn_def)
    assert result.get("a") == 265
    assert result.get("b") == 345


def test_3_greet_shrek(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_greet",
        description="Greet a person",
        parameters={"name": FunctionParameterSchema(type="string")}
    )
    result = decoder.extract_parameters("Greet shrek", fn_def)
    assert result.get("name") == "shrek"


def test_4_greet_john(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_greet",
        description="Greet a person",
        parameters={"name": FunctionParameterSchema(type="string")}
    )
    result = decoder.extract_parameters("Greet john", fn_def)
    assert result.get("name") == "john"


def test_5_reverse_string_hello(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_reverse_string",
        description="Reverse string",
        parameters={"s": FunctionParameterSchema(type="string")}
    )
    result = decoder.extract_parameters("Reverse the string 'hello'", fn_def)
    assert result.get("s") == "hello"


def test_6_reverse_string_world(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_reverse_string",
        description="Reverse string",
        parameters={"s": FunctionParameterSchema(type="string")}
    )
    result = decoder.extract_parameters("Reverse the string 'world'", fn_def)
    assert result.get("s") == "world"


def test_7_square_root_small(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_get_square_root",
        description="Square root",
        parameters={"a": FunctionParameterSchema(type="number")}
    )
    result = decoder.extract_parameters("What is the square root of 16?",
                                        fn_def)
    assert result.get("a") == 16


def test_8_square_root_large(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_get_square_root",
        description="Square root",
        parameters={"a": FunctionParameterSchema(type="number")}
    )
    result = decoder.extract_parameters("Calculate the square root of 144",
                                        fn_def)
    assert result.get("a") == 144


def test_9_regex_substitution(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_substitute_string_with_regex",
        description="Substitute with regex",
        parameters={
            "source_string": FunctionParameterSchema(type="string"),
            "regex": FunctionParameterSchema(type="string"),
            "replacement": FunctionParameterSchema(type="string")
        }
    )
    result = decoder.extract_parameters(
        "Substitute the word 'cat' with 'dog' "
        "in 'The cat sat on the mat with another cat'",
        fn_def,
    )
    assert "source_string" in result
    assert result.get("regex") == "cat"
    assert result.get("replacement") == "dog"


def test_10_edge_case_special_chars(
    mock_setup: tuple[Any, VocabularyManager],
) -> None:
    llm, vocab_manager = mock_setup
    decoder = ConstrainedJSONDecoder(llm, vocab_manager)
    fn_def = FunctionDefinition(
        name="fn_reverse_string",
        description="Reverse string with special chars",
        parameters={"s": FunctionParameterSchema(type="string")}
    )
    # Testing with special characters and numbers as requested in the subject
    result = decoder.extract_parameters(
        "Reverse the string 'hello-world! 123'",
        fn_def,
    )
    assert isinstance(result, dict)
    assert "s" in result
