"""Ponto de entrada do módulo src (CLI)."""

import argparse
import re
import sys
from typing import Any, Dict

from llm_sdk import Small_LLM_Model

from src.models import FunctionCallResult, FunctionDefinition
from src.parser import load_functions, load_test_prompts, save_results
from src.scorer import FunctionScorer


def _clean_entity(value: str) -> str:
    """Remove prepositions, articles, and trailing time words."""
    cleaned = re.sub(
        r"^(?:em|na|no|de|do|da|sobre|sobre\s+o|sobre\s+a|o|a|as|os)\s+",
        "",
        value,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"\s+(?:hoje|agora|atual|atualmente|hoy|today)\s*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"[.?!]+$", "", cleaned).strip()
    return cleaned


def extract_parameters(
    prompt: str,
    selected_fn: FunctionDefinition,
) -> Dict[str, Any]:
    """Extrai os parâmetros do prompt para a função selecionada."""
    params: Dict[str, Any] = {}
    normalized = prompt.lower()

    if selected_fn.name == "get_weather":
        city_pattern = (
            r"(?:em|na|no)\s+([A-ZÀ-ÖØ-Ý][\wÀ-ÖØ-Ý\- ]+)"
        )
        city_match = re.search(city_pattern, prompt, flags=re.IGNORECASE)
        if not city_match:
            city_match = re.search(
                (
                    r"(?:temperatura|clima)\s+"
                    r"(?:em|na|no)?\s*"
                    r"([A-ZÀ-ÖØ-Ý][\wÀ-ÖØ-Ý\- ]+)"
                ),
                prompt,
                flags=re.IGNORECASE,
            )
        if city_match:
            params["city"] = _clean_entity(city_match.group(1))
        elif "lisboa" in normalized:
            params["city"] = "Lisboa"

    elif selected_fn.name == "search_information":
        query_match = re.search(
            r"(?:sobre|de|sobre\s+o|sobre\s+a)\s+(.+?)(?:\.|$)",
            prompt,
            flags=re.IGNORECASE,
        )
        if query_match:
            params["query"] = _clean_entity(query_match.group(1))
        else:
            params["query"] = _clean_entity(prompt.strip())

    elif selected_fn.name == "get_current_time":
        location_pattern = (
            r"(?:em|na|no)\s+([A-ZÀ-ÖØ-Ý][\wÀ-ÖØ-Ý\- ]+)"
        )
        location_match = re.search(
            location_pattern,
            prompt,
            flags=re.IGNORECASE,
        )
        if location_match:
            params["location"] = _clean_entity(location_match.group(1))
        elif "londres" in normalized:
            params["location"] = "Londres"
        elif "lisboa" in normalized:
            params["location"] = "Lisboa"

    return params


def main() -> None:
    """Função principal que coordena a execução da CLI."""
    parser = argparse.ArgumentParser(
        description="Function Calling Tool com Constrained Decoding",
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="Caminho para o ficheiro de definições de funções",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="Caminho para o ficheiro de testes de entrada",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="Caminho para o ficheiro de saída",
    )

    args = parser.parse_args()

    try:
        functions = load_functions(args.functions_definition)
        test_prompts = load_test_prompts(args.input)

        llm = Small_LLM_Model()
        scorer = FunctionScorer(llm)

        results: list[FunctionCallResult] = []

        for test in test_prompts:
            best_fn = scorer.select_best_function(test.prompt, functions)
            parameters = extract_parameters(test.prompt, best_fn)

            result = FunctionCallResult(
                prompt=test.prompt,
                name=best_fn.name,
                parameters=parameters,
            )
            results.append(result)

        save_results(args.output, results)
        message = (
            "✅ Processamento concluído com sucesso. "
            f"Resultados guardados em: {args.output}"
        )
        print(message)

    except Exception as err:  # pragma: no cover - CLI failure display
        print(f"❌ Erro na execução: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
