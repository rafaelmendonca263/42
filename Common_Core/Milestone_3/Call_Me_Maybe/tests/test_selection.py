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

    def test_multi_word_locations_parameter_extraction(self) -> None:
        """Test extraction for locations with multiple words."""
        selected = self.scorer.select_best_function(
            "What is the weather like in New York?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_weather")
        params = extract_parameters("What is the weather like in New York?", selected)
        self.assertEqual(params, {"city": "New York"})

    def test_time_in_capitalized_location(self) -> None:
        """Test time query with different phrasing and capitalization."""
        selected = self.scorer.select_best_function(
            "Tell me the current time in Tokyo",
            self.functions,
        )
        self.assertEqual(selected.name, "get_current_time")
        params = extract_parameters("Tell me the current time in Tokyo", selected)
        self.assertEqual(params, {"location": "Tokyo"})

    def test_search_complex_query_parameter_extraction(self) -> None:
        """Test search parameter extraction with diverse phrasing."""
        selected = self.scorer.select_best_function(
            "Search for information about artificial intelligence.",
            self.functions,
        )
        self.assertEqual(selected.name, "search_information")
        params = extract_parameters("Search for information about artificial intelligence.", selected)
        self.assertEqual(params, {"query": "artificial intelligence"})

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
            (
                "How hot is the weather in Porto today?",
                "get_weather",
                {"city": "Porto"},
            ),
            (
                "I need information about UNESCO.",
                "search_information",
                {"query": "UNESCO"},
            ),
            (
                "What time is it now in the city of Lisbon?",
                "get_current_time",
                {"location": "Lisbon"},
            ),
        ]

        for prompt, function_name, expected in cases:
            selected = self.scorer.select_best_function(prompt, self.functions)
            self.assertEqual(selected.name, function_name)
            self.assertEqual(extract_parameters(prompt, selected), expected)


if __name__ == "__main__":
    unittest.main()
