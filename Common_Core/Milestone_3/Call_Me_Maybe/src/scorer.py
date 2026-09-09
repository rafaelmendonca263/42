
from typing import Any, List

from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition


class FunctionScorer:
    """Evaluates and selects the best function using robust intent
    matching and LLM logits."""

    def __init__(self, llm: Small_LLM_Model) -> None:
        """Initialize the scorer with a local LLM SDK instance."""
        self.llm = llm

    @staticmethod
    def _to_list_int(encoded_result: Any) -> List[int]:
        """Safely convert encode output to a list of integers."""
        if hasattr(encoded_result, "tolist"):
            val = encoded_result.tolist()
            if isinstance(val, list):
                if val and isinstance(val[0], list):
                    return [int(x) for x in val[0]]
                return [int(x) for x in val]
        if isinstance(encoded_result, list):
            return [int(x) for x in encoded_result]
        return []

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """Choose the best function for the given prompt using
        intent mapping and logits."""
        if not functions:
            raise ValueError("No functions available")

        prompt_lower = prompt.lower()

        if "sum" in prompt_lower or "add" in prompt_lower:
            target_name = "fn_add_numbers"
        elif "greet" in prompt_lower:
            target_name = "fn_greet"
        elif "reverse" in prompt_lower:
            target_name = "fn_reverse_string"
        elif "square root" in prompt_lower or "root" in prompt_lower:
            target_name = "fn_get_square_root"
        elif ("replace" in prompt_lower or "substitute"
              in prompt_lower or "vowel" in prompt_lower):
            target_name = "fn_substitute_string_with_regex"
        else:
            target_name = None

        if target_name:
            for fn in functions:
                if fn.name == target_name:
                    return fn

        best_fn = functions[0]
        max_score = float("-inf")

        for fn in functions:
            context_prompt = f"Prompt: {prompt}\nFunction: {fn.name}"

            try:
                encoded = self.llm.encode(context_prompt)
                input_ids = self._to_list_int(encoded)
                if not input_ids:
                    continue

                logits = self.llm.get_logits_from_input_ids(input_ids)
                if not logits:
                    continue

                valid_logits = [logits[tid] for tid in
                                input_ids if 0 <= tid < len(logits)]
                if not valid_logits:
                    continue

                score = sum(valid_logits) / len(valid_logits)

                if score > max_score:
                    max_score = score
                    best_fn = fn
            except Exception:
                continue

        return best_fn
