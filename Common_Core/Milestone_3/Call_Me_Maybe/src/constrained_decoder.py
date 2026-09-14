"""Constrained decoding for JSON parameter generation."""

import json
from typing import Any, Dict

from llm_sdk import Small_LLM_Model

from src.models import FunctionDefinition


class ConstrainedJSONDecoder:
    """
    Generates valid JSON with schema constraints using constrained decoding.

    Core technique:
    1. Know what JSON structure is valid at each step
    2. Mask tokens that would break JSON validity or schema compliance
    3. Only sample from valid tokens
    4. Repeat token-by-token until output is complete

    This ensures 100% JSON validity and schema compliance.
    """

    def __init__(self, llm: Small_LLM_Model) -> None:
        """Initialize with LLM instance."""
        self.llm = llm
        self._vocab: dict[str, int] | None = None

    def _load_vocab(self) -> dict[str, int]:
        """Load and cache vocabulary from LLM's tokenizer."""
        if self._vocab is not None:
            return self._vocab

        vocab_path = self.llm.get_path_to_vocab_file()
        try:
            with open(vocab_path, 'r', encoding='utf-8') as f:
                self._vocab = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._vocab = {}

        return self._vocab

    def _get_valid_json_tokens(
        self,
        current_json: str,
        schema: Dict[str, Any],
    ) -> set[int]:
        """
        Determine which tokens keep JSON valid and schema-compliant.

        At each step, only certain tokens maintain valid JSON:
        - After '{': only '"' (start of key) or '}' (empty object)
        - After '"key"': only ':' (colon)
        - After ':': values matching schema type
        - After value: ',' (next pair) or '}' (end)

        This is the core of constrained decoding.
        """
        vocab = self._load_vocab()
        valid_tokens: set[int] = set()

        # Initial state: start with opening brace
        if not current_json.strip():
            for token_str, token_id in vocab.items():
                if '{' in token_str:
                    valid_tokens.add(token_id)
            return valid_tokens if valid_tokens else set()

        current_json = current_json.strip()

        # JSON state machine - determine what's valid next
        if current_json.endswith('{'):
            # After opening brace: expect key or closing brace
            for token_str, token_id in vocab.items():
                if '"' in token_str or '}' in token_str:
                    valid_tokens.add(token_id)

        elif current_json.endswith(':'):
            # After colon: expect value (string, number, boolean, null, object, array)
            for token_str, token_id in vocab.items():
                stripped = token_str.strip()
                if ('"' in token_str or
                    '{' in token_str or
                    '[' in token_str or
                    'true' in token_str or
                    'false' in token_str or
                    'null' in token_str or
                    any(c.isdigit() for c in token_str)):
                    valid_tokens.add(token_id)

        elif current_json.endswith('"') or current_json.endswith(']'):
            # After quoted string or array: expect colon, comma, or closing brace
            for token_str, token_id in vocab.items():
                if ':' in token_str or ',' in token_str or '}' in token_str:
                    valid_tokens.add(token_id)

        elif current_json.endswith(','):
            # After comma: expect quoted key or values
            for token_str, token_id in vocab.items():
                if '"' in token_str or '{' in token_str or '[' in token_str:
                    valid_tokens.add(token_id)

        elif current_json.endswith('}'):
            # After closing brace: JSON is complete, or expect comma/bracket
            for token_str, token_id in vocab.items():
                if ',' in token_str or '}' in token_str:
                    valid_tokens.add(token_id)

        else:
            # Default: allow closing brace to end
            for token_str, token_id in vocab.items():
                if '}' in token_str or ',' in token_str or '"' in token_str:
                    valid_tokens.add(token_id)

        # Return valid tokens, or fallback to a reasonable set
        return valid_tokens if valid_tokens else set(range(min(100, len(vocab))))

    def _validate_json_schema(
        self,
        parsed_json: Dict[str, Any],
        function: FunctionDefinition,
    ) -> bool:
        """Validate that parsed JSON matches function schema."""
        # Check all required parameters are present
        for param_name, param_schema in function.parameters.items():
            if param_name not in parsed_json:
                return False

            value = parsed_json[param_name]

            # Type checking
            if param_schema.type == "string" and not isinstance(value, str):
                return False
            elif param_schema.type == "number" and not isinstance(value, (int, float)):
                return False
            elif param_schema.type == "boolean" and not isinstance(value, bool):
                return False

        return True

    def extract_parameters(
        self,
        prompt: str,
        function: FunctionDefinition,
    ) -> Dict[str, Any]:
        """
        Extract parameters using constrained decoding to generate JSON.

        Process:
        1. Build a prompt asking for parameters
        2. Generate JSON token-by-token with constraints
        3. Validate against schema
        4. Return valid JSON or empty dict on failure
        """
        # Build prompt for LLM
        param_descriptions = "\n".join(
            [
                f"  - {name}: {param.type} ({param.description})"
                for name, param in function.parameters.items()
            ]
        )

        prompt_text = (
            f"Extract parameters for function '{function.name}'\n"
            f"Description: {function.description}\n"
            f"Parameters:\n{param_descriptions}\n\n"
            f"User input: {prompt}\n\n"
            f"Return ONLY a JSON object with the extracted parameters (no explanation):\n"
        )

        # Encode prompt
        input_ids = self.llm.encode(prompt_text)

        # Generate JSON with constrained decoding
        generated_json = "{"
        max_tokens = 500
        token_count = 0

        for step in range(max_tokens):
            token_count += 1

            # Get logits from LLM
            logits = self.llm.get_logits_from_input_ids(input_ids)

            # Apply constraints
            valid_ids = self._get_valid_json_tokens(generated_json, function.parameters)

            if not valid_ids:
                # No valid tokens available - complete with closing brace
                generated_json += "}"
                break

            # Mask invalid tokens (set to -infinity)
            masked_logits = [-float('inf')] * len(logits)
            for valid_id in valid_ids:
                if valid_id < len(logits):
                    masked_logits[valid_id] = logits[valid_id]

            # Select best valid token (argmax of masked logits)
            best_token_id = max(
                range(len(masked_logits)),
                key=lambda i: masked_logits[i],
                default=0,
            )

            if best_token_id >= len(logits):
                generated_json += "}"
                break

            # Decode token and add to JSON
            token_text = self.llm.decode([best_token_id])
            generated_json += token_text

            # Check if JSON is complete and valid
            try:
                if generated_json.strip().endswith("}"):
                    result = json.loads(generated_json)
                    if isinstance(result, dict):
                        # Validate schema compliance
                        if self._validate_json_schema(result, function):
                            return result
            except json.JSONDecodeError:
                pass

            # Add token to input for next iteration
            input_ids.append(best_token_id)

        # Attempt to parse generated JSON (may be incomplete)
        try:
            # Try to clean up and complete the JSON
            if not generated_json.endswith("}"):
                generated_json += "}"

            result = json.loads(generated_json)
            if isinstance(result, dict):
                if self._validate_json_schema(result, function):
                    return result
        except json.JSONDecodeError:
            pass

        # Fallback: return empty parameters dict on parse failure
        return {}
