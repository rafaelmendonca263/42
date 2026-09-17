from typing import List
import numpy as np
from llm_sdk import Small_LLM_Model  # type: ignore
from src.models import FunctionDefinition
from src.structure import VocabularyManager


class ConstrainedFunctionSelector:
    """Selects the best function using LLM logits
    with strict prefix constraints."""

    def __init__(
        self,
        llm: Small_LLM_Model,
        functions: List[FunctionDefinition],
        vocab_manager: VocabularyManager,
    ) -> None:
        self.llm = llm
        self.vocab_manager = vocab_manager
        self.valid_names = [fn.name for fn in functions]

        # Maps and cleans the vocabulary once at startup
        self._token_str_map: dict[int, str] = {}
        for token_str, token_id in self.vocab_manager.vocab.items():
            clean = token_str.lstrip('Ġ ')
            self._token_str_map[int(token_id)] = clean

    def _get_valid_token_ids(self, partial_name: str) -> set[int]:
        """Returns token IDs that build a valid function
        name from available functions efficiently."""
        valid_token_ids: set[int] = set()

        for fn_name in self.valid_names:
            if fn_name.startswith(partial_name):
                rem = fn_name[len(partial_name):]
                if rem:
                    first_char = rem[0]
                    candidate_tokens = (
                        self.vocab_manager.char_to_tokens.get(first_char, [])
                    )
                    for token_id in candidate_tokens:
                        clean = self._token_str_map.get(token_id, "")
                        if not clean:
                            continue
                        if rem.startswith(clean) or clean.startswith(rem):
                            valid_token_ids.add(token_id)

        return valid_token_ids

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """Selects the best function using constrained logits
        decoding with clear guidance."""
        if not functions:
            raise ValueError("No functions available to select from")

        fn_map = {fn.name: fn for fn in functions}
        self.valid_names = list(fn_map.keys())

        function_list = "\n".join(
            [f"- {fn.name}: {fn.description}" for fn in functions]
        )

        # Refined prompt to better guide the Small LLM in making the choice
        prompt_text = (
            f"Analyze the user request carefully and select the"
            f"best matching function.\n\n"
            f"Available functions:\n{function_list}\n\n"
            f"User request: {prompt}\n\n"
            f"Instructions: Output ONLY the exact name of "
            f"the correct function.\n"
            f"Function name:"
        )

        input_ids = self.llm.encode(prompt_text).tolist()[0]
        selected_name = ""
        max_tokens = 30

        for _ in range(max_tokens):
            logits = self.llm.get_logits_from_input_ids(input_ids)
            logits_arr = np.array(logits)
            if logits_arr.ndim > 1:
                logits_arr = logits_arr[-1]

            valid_ids = self._get_valid_token_ids(selected_name)
            if not valid_ids:
                break

            masked_logits = np.full(len(logits_arr), -np.inf)
            valid_array = [v for v in valid_ids if v < len(logits_arr)]
            if valid_array:
                masked_logits[valid_array] = logits_arr[valid_array]

            best_token_id = int(np.argmax(masked_logits))
            if best_token_id >= len(logits_arr):
                break

            token_text = self.llm.decode([best_token_id]).lstrip('Ġ ')
            selected_name += token_text

            if selected_name in fn_map:
                return fn_map[selected_name]

            input_ids.append(best_token_id)

        # Fallback para correspondência parcial mais próxima
        for name, fn in fn_map.items():
            if selected_name and name.startswith(selected_name):
                return fn

        return functions[0]
