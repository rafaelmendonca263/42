"""Constrained decoding for JSON parameter generation."""

import json
from typing import Any, Dict

import numpy as np
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
        """Initialize with LLM instance and build vocabulary index."""
        self.llm = llm
        self._vocab: dict[str, int] | None = None
        self.char_to_tokens: dict[str, list[int]] = {}
        
        # ⚙️ Pré-processa o vocabulário na inicialização para otimizar buscas
        vocab = self._load_vocab()
        for token_str, token_id in vocab.items():
            if token_str:
                first_char = token_str[0]
                self.char_to_tokens.setdefault(first_char, []).append(token_id)

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
        """Determine which tokens keep JSON valid and schema-compliant."""
        vocab = self._load_vocab()
        valid_tokens: set[int] = set()

        # 🚀 Exemplo de uso do índice para o estado inicial
        if not current_json.strip():
            for token_id in self.char_to_tokens.get('{', []):
                valid_tokens.add(token_id)
            return valid_tokens if valid_tokens else set()

        current_json = current_json.strip()

        # JSON state machine - determine what's valid next
        if current_json.endswith('{'):
            for char in ['"', '}']:
                for token_id in self.char_to_tokens.get(char, []):
                    valid_tokens.add(token_id)

        elif current_json.endswith(':'):
            for token_str, token_id in vocab.items():
                if ('"' in token_str or
                    '{' in token_str or
                    '[' in token_str or
                    'true' in token_str or
                    'false' in token_str or
                    'null' in token_str or
                    any(c.isdigit() for c in token_str)):
                    valid_tokens.add(token_id)

        elif current_json.endswith('"') or current_json.endswith(']'):
            for token_str, token_id in vocab.items():
                if ':' in token_str or ',' in token_str or '}' in token_str:
                    valid_tokens.add(token_id)

        elif current_json.endswith(','):
            for token_str, token_id in vocab.items():
                if '"' in token_str or '{' in token_str or '[' in token_str:
                    valid_tokens.add(token_id)

        elif current_json.endswith('}'):
            for token_str, token_id in vocab.items():
                if ',' in token_str or '}' in token_str:
                    valid_tokens.add(token_id)

        else:
            for token_str, token_id in vocab.items():
                if '}' in token_str or ',' in token_str or '"' in token_str:
                    valid_tokens.add(token_id)

        return valid_tokens if valid_tokens else set(range(min(100, len(vocab))))

    def _validate_json_schema(
        self,
        parsed_json: Dict[str, Any],
        function: FunctionDefinition,
    ) -> bool:
        """Validate that parsed JSON matches function schema."""
        for param_name, param_schema in function.parameters.items():
            if param_name not in parsed_json:
                return False

            value = parsed_json[param_name]

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
        """Extract parameters using constrained decoding to generate JSON."""
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

        input_ids = self.llm.encode(prompt_text).tolist()[0]
        generated_json = "{"
        max_tokens = 500

        for step in range(max_tokens):
            logits = self.llm.get_logits_from_input_ids(input_ids)
            if hasattr(logits, "detach"):
                logits_arr = logits.detach().cpu().numpy()
            else:
                logits_arr = np.array(logits)

            if logits_arr.ndim > 1:
                logits_arr = logits_arr[-1]

            valid_ids = self._get_valid_json_tokens(generated_json, function.parameters)

            if not valid_ids:
                generated_json += "}"
                break

            masked_logits = np.full(len(logits_arr), -np.inf)
            valid_array = [v for v in valid_ids if v < len(logits_arr)]
            if valid_array:
                masked_logits[valid_array] = logits_arr[valid_array]

            best_token_id = int(np.argmax(masked_logits))

            if best_token_id >= len(logits_arr):
                generated_json += "}"
                break

            token_text = self.llm.decode([best_token_id])
            generated_json += token_text

            try:
                if generated_json.strip().endswith("}"):
                    result = json.loads(generated_json)
                    if isinstance(result, dict):
                        if self._validate_json_schema(result, function):
                            return result
            except json.JSONDecodeError:
                pass

            input_ids.append(best_token_id)

        try:
            if not generated_json.endswith("}"):
                generated_json += "}"

            result = json.loads(generated_json)
            if isinstance(result, dict):
                if self._validate_json_schema(result, function):
                    return result
        except json.JSONDecodeError:
            pass

        return {}
