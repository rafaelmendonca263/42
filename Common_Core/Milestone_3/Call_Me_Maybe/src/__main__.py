import argparse
import sys

from llm_sdk import Small_LLM_Model  # type: ignore

from src.constrained_decoder import ConstrainedJSONDecoder
from src.llm_selector import ConstrainedFunctionSelector
from src.models import FunctionCallResult
from src.parser import load_functions, load_test_prompts, save_results
from src.structure import VocabularyManager


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
        vocab_path = llm.get_path_to_vocab_file()

        vocab_manager = VocabularyManager(vocab_path)

        selector = ConstrainedFunctionSelector(llm, functions, vocab_manager)
        decoder = ConstrainedJSONDecoder(llm, vocab_manager)

        results: list[FunctionCallResult] = []

        for i, test in enumerate(test_prompts, 1):
            best_fn = selector.select_best_function(test.prompt, functions)
            parameters = decoder.extract_parameters(test.prompt, best_fn)

            result = FunctionCallResult(
                prompt=test.prompt,
                name=best_fn.name,
                parameters=parameters,
            )
            results.append(result)

        save_results(args.output, results)

    except Exception as err:
        print(f"Execution error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
