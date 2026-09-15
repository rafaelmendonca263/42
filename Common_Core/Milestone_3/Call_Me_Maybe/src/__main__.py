"""Entry point for the src module (CLI)."""

import argparse
import sys

from llm_sdk import Small_LLM_Model

from src.constrained_decoder import ConstrainedJSONDecoder
from src.llm_selector import ConstrainedFunctionSelector
from src.models import FunctionCallResult
from src.parser import load_functions, load_test_prompts, save_results


def main() -> None:
    """Main function that coordinates CLI execution."""
    parser = argparse.ArgumentParser(
        description="Function Calling Tool with Constrained Decoding",
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="Path to the function definition file",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="Path to the input test file",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="Path to the output file",
    )

    args = parser.parse_args()

    try:
        functions = load_functions(args.functions_definition)
        test_prompts = load_test_prompts(args.input)

        llm = Small_LLM_Model()
        selector = ConstrainedFunctionSelector(llm)
        decoder = ConstrainedJSONDecoder(llm)

        results: list[FunctionCallResult] = []

        for test in test_prompts:
            # 🎯 Seleção da função e extração de parâmetros totalmente por decodificação restrita e NumPy
            best_fn = selector.select_best_function(test.prompt, functions)
            parameters = decoder.extract_parameters(test.prompt, best_fn)

            result = FunctionCallResult(
                prompt=test.prompt,
                name=best_fn.name,
                parameters=parameters,
            )
            results.append(result)

        save_results(args.output, results)
        print(f"✅ Processing completed successfully. Results saved to: {args.output}")

    except Exception as err:
        print(f"❌ Execution error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
