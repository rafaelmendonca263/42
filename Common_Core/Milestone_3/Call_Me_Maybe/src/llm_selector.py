"""LLM-based function selection using constrained decoding with a Trie."""

import json
from typing import List

import numpy as np
from llm_sdk import Small_LLM_Model

from src.models import FunctionDefinition
from src.structure import Trie


class ConstrainedFunctionSelector:
    """Selects the best function using the LLM with constrained decoding backed by a Trie."""

    def __init__(self, llm: Small_LLM_Model, functions: List[FunctionDefinition]) -> None:
        """Initialize with LLM instance, build vocabulary index, and construct the Trie."""
        self.llm = llm
        self._vocab: dict[str, int] | None = None
        self.char_to_tokens: dict[str, list[int]] = {}

        # 🪵 Constrói a Trie uma única vez na inicialização
        self.trie = Trie()
        for fn in functions:
            self.trie.insert(fn.name)

        # ⚙️ Pré-processa o vocabulário
        vocab = self._load_vocab()
        for token_str, token_id in vocab.items():
            if token_str:
                first_char = token_str[0]
                self.char_to_tokens.setdefault(first_char, []).append(token_id)

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

    def _get_valid_token_ids(self, partial_name: str) -> set[int]:
        """Get token IDs using the pre-built Trie structure."""
        valid_token_ids: set[int] = set()

        current_node = self.trie.search_prefix(partial_name)
        if current_node:
            for char in current_node.children:
                for token_id in self.char_to_tokens.get(char, []):
                    valid_token_ids.add(token_id)

        return valid_token_ids

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """Select best function using LLM logits with constrained decoding via Trie."""
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
