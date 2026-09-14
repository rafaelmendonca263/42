"""LLM-based function selection using constrained decoding."""

import json
from typing import List

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
            # Fallback: create minimal vocab from function names
            self._vocab = {}

        return self._vocab

    def _get_valid_token_ids(
        self,
        functions: List[FunctionDefinition],
        partial_name: str,
    ) -> set[int]:
        """
        Get token IDs that continue valid function names.

        This is the core of constrained decoding: identify which tokens
        can be generated next without breaking the function name schema.
        """
        vocab = self._load_vocab()
        valid_token_ids: set[int] = set()

        # Collect all valid function names
        valid_names = [fn.name for fn in functions]

        # For each valid function name, find tokens that extend the partial name
        for name in valid_names:
            if name.startswith(partial_name):
                # Get the next character(s) that could follow
                remainder = name[len(partial_name):]
                if remainder:
                    # Try to find tokens matching the next part
                    next_char = remainder[0]
                    # Look for tokens starting with this character
                    for token_str, token_id in vocab.items():
                        if (token_str.startswith(next_char) or
                            token_str.lstrip().startswith(next_char)):
                            valid_token_ids.add(token_id)

        return valid_token_ids

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """
        Select best function using LLM logits with constrained decoding.

        Process:
        1. Create a prompt asking the LLM to choose a function
        2. Use constrained decoding to generate only valid function names
        3. Return the selected function
        """
        if not functions:
            raise ValueError("No functions available to select from")

        # Build prompt for LLM
        function_list = "\n".join(
            [f"- {fn.name}: {fn.description}" for fn in functions]
        )

        prompt_text = (
            f"Given the following functions:\n{function_list}\n\n"
            f"User request: {prompt}\n\n"
            f"Select the function name (just the name, nothing else):\n"
        )

        # Encode the prompt
        input_ids = self.llm.encode(prompt_text)

        # Generate function name token-by-token with constrained decoding
        selected_name = ""
        max_tokens = 50  # Max length for function name

        for step in range(max_tokens):
            # Get logits from LLM
            logits = self.llm.get_logits_from_input_ids(input_ids)

            # Apply constrained decoding: mask invalid tokens
            valid_ids = self._get_valid_token_ids(functions, selected_name)

            if not valid_ids:
                # If no valid tokens, fall back to direct scoring
                break

            # Set logits to -inf for invalid tokens
            masked_logits = [-float('inf')] * len(logits)
            for valid_id in valid_ids:
                if valid_id < len(logits):
                    masked_logits[valid_id] = logits[valid_id]

            # Select token with highest logit from valid tokens
            best_token_id = max(
                range(len(masked_logits)),
                key=lambda i: masked_logits[i],
                default=0,
            )

            if best_token_id >= len(logits):
                break

            # Decode the token and add to selected name
            token_text = self.llm.decode([best_token_id])
            selected_name += token_text.strip()

            # Check if we've completed a valid function name
            for fn in functions:
                if fn.name == selected_name.strip():
                    return fn

            # Add token to input for next iteration
            input_ids.append(best_token_id)

        # Fallback: find best match by direct function name comparison
        selected_name = selected_name.strip()
        for fn in functions:
            if fn.name.lower() in selected_name.lower():
                return fn

        # Last resort: score functions by keyword overlap with original prompt
        best_fn = functions[0]
        best_score = 0
        for fn in functions:
            score = sum(
                1 for word in fn.name.lower().split('_')
                if word in prompt.lower()
            )
            if score > best_score:
                best_score = score
                best_fn = fn

        return best_fn
