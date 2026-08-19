import unittest

from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition, FunctionParameterSchema
from src.scorer import FunctionScorer


class TestFunctionSelection(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = FunctionScorer(Small_LLM_Model())
        self.functions = [
            FunctionDefinition(
                name="get_weather",
                description="Devolve a temperatura e o clima de uma cidade.",
                parameters={
                    "city": FunctionParameterSchema(
                        type="string",
                        description="Nome da cidade",
                    )
                },
            ),
            FunctionDefinition(
                name="search_information",
                description=(
                    "Pesquisa informação geral sobre um tema "
                    "ou entidade."
                ),
                parameters={
                    "query": FunctionParameterSchema(
                        type="string",
                        description="Termo ou entidade a procurar",
                    )
                },
            ),
            FunctionDefinition(
                name="get_current_time",
                description="Devolve a hora atual de uma localização.",
                parameters={
                    "location": FunctionParameterSchema(
                        type="string",
                        description="Localização para obter a hora",
                    )
                },
            ),
        ]

    def test_weather_prompt_selects_weather_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Qual é a temperatura em Lisboa hoje?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_weather")

    def test_search_prompt_selects_search_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Procura informação sobre o Rio de Janeiro.",
            self.functions,
        )
        self.assertEqual(selected.name, "search_information")

    def test_time_prompt_selects_time_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Qual é a hora atual em Londres?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_current_time")

    def test_weather_variant_prompt_selects_weather_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Quão quente está o clima em Porto hoje?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_weather")

    def test_search_variant_prompt_selects_search_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Preciso de informações sobre a UNESCO.",
            self.functions,
        )
        self.assertEqual(selected.name, "search_information")

    def test_time_variant_prompt_selects_time_function(self) -> None:
        selected = self.scorer.select_best_function(
            "Que horas são agora na cidade de Lisboa?",
            self.functions,
        )
        self.assertEqual(selected.name, "get_current_time")


if __name__ == "__main__":
    unittest.main()
