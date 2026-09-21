import json
import re
from typing import Any, Dict

import numpy as np
from llm_sdk import Small_LLM_Model  # type: ignore

from src.models import FunctionDefinition
from src.structure import VocabularyManager


def safe_loads(s: str) -> Any:
    """Parse JSON string safely, allowing trailing commas,
    quotes, and regex escape fixes."""
    cleaned = re.sub(r',\s*([\]}])', r'\1', s)
    cleaned = cleaned.replace("\\'", "'")

    def fix_escapes(match: re.Match[str]) -> str:
        escape_char = match.group(1)
        if escape_char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u']:
            return '\\' + escape_char
        return '\\\\' + escape_char

    cleaned = re.sub(r'\\([^"\\])', fix_escapes, cleaned)
    return json.loads(cleaned)


class ConstrainedJSONDecoder:
    """Generates valid JSON with schema
    constraints using constrained decoding."""

    def __init__(
        self,
        llm: Small_LLM_Model,
        vocab_manager: VocabularyManager,
        max_tokens: int = 300,
    ) -> None:
        self.llm = llm
        self.vocab_manager = vocab_manager
        self.max_tokens = max_tokens

        self._token_str_map: dict[int, str] = {}
        for token_str, token_id in self.vocab_manager.vocab.items():
            clean = token_str.lstrip('Ġ ')
            self._token_str_map[token_id] = clean

    def sample_token(self, logits: Any, valid_tokens: set[int]) -> int:
        if hasattr(logits, "detach"):
            logits_arr = logits.detach().cpu().numpy()
        else:
            logits_arr = np.array(logits)

        if logits_arr.ndim > 1:
            logits_arr = logits_arr[-1]

        masked_logits = np.full(len(logits_arr), -np.inf)
        valid_array = [v for v in valid_tokens if v < len(logits_arr)]

        if valid_array:
            masked_logits[valid_array] = logits_arr[valid_array]
            return int(np.argmax(masked_logits))

        return int(np.argmax(logits_arr))

    def get_tokens_for_chars(self, chars: list[str]) -> set[int]:
        valid_tokens: set[int] = set()
        for char in chars:
            if char in self.vocab_manager.char_to_tokens:
                valid_tokens.update(self.vocab_manager.char_to_tokens[char])
        return valid_tokens

    def get_valid_key_tokens(self,
                             prefix: str,
                             pending_params: list[str]) -> set[int]:
        """Filter tokens so candidate keys can only
        match pending parameter names efficiently."""
        valid_tokens: set[int] = set()

        for param in pending_params:
            if param.startswith(prefix):
                rem = param[len(prefix):]
                if rem:
                    first_char = rem[0]
                    candidate_tokens = (
                        self.vocab_manager.char_to_tokens.get(first_char, [])
                    )
                    for token_id in candidate_tokens:
                        clean = self._token_str_map.get(token_id, "")
                        candidate = prefix + clean
                        if (
                            param.startswith(candidate)
                            or candidate.startswith(param + '"')
                        ):
                            valid_tokens.add(token_id)
                elif prefix == param:
                    valid_tokens.update(self.get_tokens_for_chars(['"']))

        return valid_tokens

    def get_valid_json_tokens(
        self,
        current_json: str,
        function: FunctionDefinition,
        prompt: str = "",
    ) -> set[int]:
        cleaned = current_json.strip()

        if not cleaned:
            return set(self.llm.encode("{").tolist()[0])

        in_str = False
        esc = False
        for ch in cleaned:
            if esc:
                esc = False
            elif ch == '\\' and in_str:
                esc = True
            elif ch == '"':
                in_str = not in_str

        all_params = list(function.parameters.keys())
        found_keys = re.findall(r'"([^"]+)"\s*:', cleaned)
        existing_keys = [k for k in found_keys if k in all_params]
        pending_params = [p for p in all_params if p not in existing_keys]

        # CASE A: Inside string
        if in_str:
            last_quote_idx = cleaned.rfind('"')
            before_quote = cleaned[:last_quote_idx].strip()
            is_key = (
                before_quote == ""
                or before_quote.endswith("{")
                or before_quote.endswith(",")
            )

            if is_key:
                current_key_prefix = cleaned[last_quote_idx + 1:]
                return self.get_valid_key_tokens(current_key_prefix,
                                                 pending_params)
            else:
                valid_tokens = set()
                allowed_chars = set(prompt).union(
                    set('abcdefghijklmnopqrstuvwxyzABC'
                        'DEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    .union(set(' _-.,!?/\\()[]{}*+?|^$@#%&=:;"\'\n\t'))
                )
                for char in allowed_chars:
                    valid_tokens.update(self.get_tokens_for_chars([char]))
                return valid_tokens

        # CASE B: Outside string
        stripped_no_ws = cleaned.rstrip()
        last_char = stripped_no_ws[-1] if stripped_no_ws else ""

        if last_char == '}':
            return set()

        if last_char in ['{', ',']:
            if pending_params:
                return self.get_tokens_for_chars(['"'])
            return self.get_tokens_for_chars(['}'])

        if last_char == ':':
            active_param = found_keys[-1] if found_keys else None
            param_type = "string"
            if active_param and active_param in function.parameters:
                param_type = function.parameters[active_param].type

            if param_type == "number":
                target_chars = [str(i) for i in range(10)] + ['.', '-']
            elif param_type == "boolean":
                target_chars = ['t', 'f', 'T', 'F']
            else:
                target_chars = ['"']

            return self.get_tokens_for_chars(target_chars)

        if last_char == '"':
            last_q = cleaned.rfind('"')
            second_q = cleaned.rfind('"', 0, last_q)
            if second_q != -1:
                before_this_string = cleaned[:second_q].strip()
                is_key_string = (
                    before_this_string == ""
                    or before_this_string.endswith("{")
                    or before_this_string.endswith(",")
                )

                if is_key_string:
                    return self.get_tokens_for_chars([':'])

            if pending_params:
                return self.get_tokens_for_chars([','])
            return self.get_tokens_for_chars(['}'])

        if last_char.isdigit() or last_char in ['.', '-']:
            if pending_params:
                target_chars = [str(i) for i in range(10)] + ['.', ',']
            else:
                target_chars = [str(i) for i in range(10)] + ['.', '}']
            return self.get_tokens_for_chars(target_chars)

        if pending_params:
            return self.get_tokens_for_chars([','])
        return self.get_tokens_for_chars(['}'])

    def validate_json_schema(
        self,
        parsed_json: Dict[str, Any],
        function: FunctionDefinition,
    ) -> bool:
        for param_name, param_schema in function.parameters.items():
            if param_name not in parsed_json:
                return False

            value = parsed_json[param_name]
            if param_schema.type == "string" and not isinstance(value, str):
                return False
            elif param_schema.type == "number" and not isinstance(value,
                                                                  (int,
                                                                   float)):
                return False
            elif param_schema.type == "boolean" and not isinstance(value,
                                                                   bool):
                return False

        return True

    def extract_parameters(
        self,
        prompt: str,
        function: FunctionDefinition,
    ) -> dict[str, Any]:
        """Extracts parameters with strict schema enforcement."""
        if not function.parameters:
            return {}

        param_details = ", ".join(
            [f"'{k}' ({v.type})" for k, v in function.parameters.items()]
        )

        prompt_text = (
            "Extract the exact arguments for function "
            f"'{function.name}' "
            "based on the user input.\n"
            f"Required parameters: [{param_details}]\n"
            f"User input: {prompt}\n"
            "JSON response:"
        )

        prompt_ids = self.llm.encode(prompt_text).tolist()[0]
        start_brace_ids = self.llm.encode("{").tolist()[0]
        start_brace_id = start_brace_ids[-1]

        input_ids = prompt_ids + [start_brace_id]
        generated_part_ids = [start_brace_id]

        for _ in range(self.max_tokens):
            generated_text = self.llm.decode(generated_part_ids)

            try:
                stripped_json = generated_text.strip()
                if (
                    stripped_json.startswith("{")
                    and stripped_json.endswith("}")
                ):
                    result = safe_loads(stripped_json)
                    if (
                        isinstance(result, dict)
                        and self.validate_json_schema(result,
                                                      function)
                    ):
                        return result
            except Exception:
                pass

            logits = self.llm.get_logits_from_input_ids(input_ids)
            valid_tokens = self.get_valid_json_tokens(generated_text,
                                                      function,
                                                      prompt)

            if not valid_tokens:
                break

            next_token_id = self.sample_token(logits, valid_tokens)
            input_ids.append(next_token_id)
            generated_part_ids.append(next_token_id)

        try:
            final_text = self.llm.decode(generated_part_ids).strip()
            if final_text.startswith("{") and not final_text.endswith("}"):
                final_text += "}"
            parsed = safe_loads(final_text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        return {}
