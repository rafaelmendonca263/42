"""LLM-based function selection using constrained decoding."""

import json
from typing import List

import numpy as np
from llm_sdk import Small_LLM_Model

from src.models import FunctionDefinition


class ConstrainedFunctionSelector:
    """
    Selects the best function using the LLM with constrained decoding.

    This implementation:
    1. Uses the LLM's logits (not heuristics) to score function names
    2. Applies constrained decoding to ensure only valid function names are generated
    3. Uses the vocabulary to restrict token generation
    """

    def __init__(self, llm: Small_LLM_Model) -> None:
        """Initialize with LLM instance."""
        self.llm = llm
        self._vocab: dict[str, int] | None = None

    def _load_vocab(self) -> dict[str, int]:
        """Load vocabulary from LLM's vocab file."""
        if self._vocab is not None:
            return self._vocab

        vocab_path = self.llm.get_path_to_vocab_file()
        try:
            with open(vocab_path, 'r', encoding='utf-8') as f:
                self._vocab = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._vocab = {}

        return self._vocab

    def _get_valid_token_ids(
        self,
        functions: List[FunctionDefinition],
        partial_name: str,
    ) -> set[int]:
        """Get token IDs that continue valid function names."""
        vocab = self._load_vocab()
        valid_token_ids: set[int] = set()

        valid_names = [fn.name for fn in functions]

        for name in valid_names:
            if name.startswith(partial_name):
                remainder = name[len(partial_name):]
                if remainder:
                    next_char = remainder[0]
                    for token_str, token_id in vocab.items():
                        if ((token_str.startswith(next_char) or
                             token_str.lstrip().startswith(next_char))):
                            valid_token_ids.add(token_id)

        return valid_token_ids

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """Select best function using LLM logits with constrained decoding."""
        if not functions:
            raise ValueError("No functions available to select from")

        function_list = "\n".join(
            [f"- {fn.name}: {fn.description}" for fn in functions]
        )

        prompt_text = (
            f"Given the following functions:\n{function_list}\n\n"
            f"User request: {prompt}\n\n"
            f"Select the function name (just the name, nothing else):\n"
        )

        input_ids = self.llm.encode(prompt_text).tolist()[0]
        selected_name = ""
        max_tokens = 50

        for step in range(max_tokens):
            logits = self.llm.get_logits_from_input_ids(input_ids)
            if hasattr(logits, "detach"):
                logits_arr = logits.detach().cpu().numpy()
            else:
                logits_arr = np.array(logits)

            if logits_arr.ndim > 1:
                logits_arr = logits_arr[-1] 

            valid_ids = self._get_valid_token_ids(functions, selected_name)

            if not valid_ids:
                break

            # 🛑 Máscara com NumPy
            masked_logits = np.full(len(logits_arr), -np.inf)
            valid_array = [v for v in valid_ids if v < len(logits_arr)]
            if valid_array:
                masked_logits[valid_array] = logits_arr[valid_array]

            # 🎯 Seleção do melhor token com np.argmax()
            best_token_id = int(np.argmax(masked_logits))

            if best_token_id >= len(logits_arr):
                break

            token_text = self.llm.decode([best_token_id])
            selected_name += token_text.strip()

            for fn in functions:
                if fn.name == selected_name.strip():
                    return fn

            input_ids.append(best_token_id)

        selected_name = selected_name.strip()
        for fn in functions:
            if fn.name.lower() in selected_name.lower():
                return fn

        return functions[0]
