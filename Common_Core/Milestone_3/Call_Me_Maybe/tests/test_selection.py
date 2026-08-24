import unittest

from llm_sdk import Small_LLM_Model
from src.__main__ import extract_parameters
from src.models import FunctionDefinition, FunctionParameterSchema
from src.scorer import FunctionScorer


class TestFunctionSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = FunctionScorer(Small_LLM_Model())
        self.functions = [
            FunctionDefinition(
                name="get_weather",
                description="Returns the temperature and weather for a city.",
                parameters={
                    "city": FunctionParameterSchema(
                        type="string",
                        description="City name",
                    )
                },
            ),
            FunctionDefinition(
                name="search_information",
                description=(
                    "Searches for general information about a topic "
                    "or entity."
                ),
                parameters={
                    "query": FunctionParameterSchema(
                        type="string",
                        description="Term or entity to search for",
                    )
                },
            ),
            FunctionDefinition(
                name="get_current_time",
                description="Returns the current time for a location.",
                parameters={
                    "location": FunctionParameterSchema(
                        type="string",
                        description="Location to get the time for",
                    )
                },
            ),
        ]

    def test_weather_prompt_selects_weather_function(self) -> None:
        selected = self.scorer.select_best_function(
            "What is the temperature in Lisbon today?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_weather")

    def test_search_prompt_selects_search_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Search for information about Rio de Janeiro.",
            self.functions,
        )
        self.assertEqual(selected.name, "search_information")

    def test_time_prompt_selects_time_function(self) -> None:
        selected = self.scorer.select_best_function(
            "What is the current time in London?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_current_time")

    def test_weather_variant_prompt_selects_weather_function(self) -> None:
        selected = self.scorer.select_best_function(
            "How hot is the weather in Porto today?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_weather")

    def test_search_variant_prompt_selects_search_function(self) -> None:
        selected = self.scorer.select_best_function(
            "I need information about UNESCO.",
            self.functions,
        )
        self.assertEqual(selected.name, "search_information")

    def test_time_variant_prompt_selects_time_function(self) -> None:
        selected = self.scorer.select_best_function(
            "What time is it now in the city of Lisbon?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_current_time")

    def test_extract_parameters_removes_articles_and_time_words(self) -> None:
        cases = [
            (
                "What is the temperature in Lisbon today?",
                "get_weather",
                {"city": "Lisbon"},
            ),
            (
                "Search for information about Rio de Janeiro.",
                "search_information",
                {"query": "Rio de Janeiro"},
            ),
            (
                "What is the current time in London?",
                "get_current_time",
                {"location": "London"},
            ),
        ]

        for prompt, function_name, expected in cases:
            selected = self.scorer.select_best_function(prompt, self.functions)
            self.assertEqual(selected.name, function_name)
            self.assertEqual(extract_parameters(prompt, selected), expected)


if __name__ == "__main__":
    unittest.main()
