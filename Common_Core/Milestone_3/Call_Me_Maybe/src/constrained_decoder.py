import json
import re
from typing import Any, Dict

import numpy as np
from llm_sdk import Small_LLM_Model  # type: ignore

from src.models import FunctionDefinition
from src.structure import VocabularyManager


def safe_loads(s: str) -> Any:
    """Parse JSON safely, fixing trailing commas and backslashes."""
    cleaned = re.sub(r',\s*([\]}])', r'\1', s)
    cleaned = cleaned.replace("\\'", "'")

    def repl(m: re.Match[str]) -> str:
        bs = m.group(1)
        next_char = m.group(2)
        valid_escapes = {'"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u'}
        if next_char in valid_escapes:
            return bs + next_char
        return '\\\\' + next_char

    cleaned = re.sub(r'(\\)(.)', repl, cleaned)

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
            clean = token_str.replace("Ġ", " ")
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
        for token_id, clean_str in self._token_str_map.items():
            if not clean_str:
                continue
            for char in chars:
                if clean_str.startswith(char) or char.startswith(clean_str):
                    valid_tokens.add(token_id)
        return valid_tokens

    def get_valid_key_tokens(
        self,
        current_key_prefix: str,
        pending_params: list[str],
    ) -> set[int]:
        """Returns token IDs that build a valid pending parameter key."""
        valid_token_ids: set[int] = set()
        for param in pending_params:
            if param.startswith(current_key_prefix):
                rem = param[len(current_key_prefix):]
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
                if param == current_key_prefix:
                    valid_token_ids.update(self.get_tokens_for_chars(['"']))
        return valid_token_ids

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
            if cleaned.endswith('\\'):
                escape_chars = ['"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u']
                return self.get_tokens_for_chars(escape_chars)

            last_quote_idx = cleaned.rfind('"')
            before_quote = cleaned[:last_quote_idx].strip()
            is_key = (
                before_quote == ""
                or before_quote.endswith("{")
                or before_quote.endswith(",")
            )

            if is_key:
                current_key_prefix = cleaned[last_quote_idx + 1:]
                return self.get_valid_key_tokens(
                    current_key_prefix,
                    pending_params
                )
            else:
                valid_tokens = set()
                allowed_chars = set(prompt).union(
                    set('abcdefghijklmnopqrstuvwxyzABC'
                        'DEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    .union(set(' _-.,!?/\\()[]{}*+?|^$@#%&=:\'\n\t"'))
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

            if param_type in ("number", "integer"):
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
            elif param_schema.type == "number":
                if not isinstance(value, (int, float)):
                    return False
                if isinstance(value, int):
                    parsed_json[param_name] = float(value)
            elif param_schema.type == "integer":
                if not isinstance(value, int) or isinstance(value, bool):
                    return False
            elif param_schema.type == "boolean" and not isinstance(value,
                                                                   bool):
                return False

        return True

    def refine_string_parameters(
        self,
        parsed_json: Dict[str, Any],
        prompt: str,
        function: FunctionDefinition,
    ) -> Dict[str, Any]:
        """Refines string parameters generically by
        grounding them against prompt patterns."""
        refined = parsed_json.copy()

        for param_name, param_schema in function.parameters.items():
            if param_schema.type != "string":
                continue

            # 1. Query / SQL parameters: extract
            # exact quoted string from prompt
            if "query" in param_name.lower() or "sql" in param_name.lower():
                matches = re.findall(r"['\"]([^'\"]+)['\"]", prompt)
                if matches:
                    for m in matches:
                        if len(m) > 3:
                            refined[param_name] = m
                            break

            # 2. Template parameters: extract after format prefixes or quotes
            elif "template" in param_name.lower():
                if "Format template:" in prompt:
                    refined[param_name] = prompt.split("Format template:",
                                                       1)[1].strip()
                else:
                    matches = re.findall(r"['\"]([^'\"]+)['\"]", prompt)
                    if matches:
                        refined[param_name] = matches[0]

            # 3. Path / File parameters
            elif "path" in param_name.lower() or "file" in param_name.lower():
                words = prompt.split()
                for word in words:
                    if '/' in word or '\\' in word or '.' in word:
                        cleaned_word = word.strip(".,;:?!'\"")
                        if (len(cleaned_word) > 2
                            and not cleaned_word.lower() in ("encoding",
                                                             "with", "at")):
                            refined[param_name] = cleaned_word
                            break

            # 4. Encoding parameters
            elif "encoding" in param_name.lower():
                encodings = ["utf-8", "latin-1", "ascii", "utf16", "utf-16"]
                for enc in encodings:
                    if enc in prompt.lower():
                        refined[param_name] = enc
                        break

            # 5. Database parameters
            elif "database" in param_name.lower():
                if "production" in prompt.lower():
                    refined[param_name] = "production"
                elif "system" in prompt.lower():
                    refined[param_name] = "system"

        return refined

    def extract_parameters(
        self,
        prompt: str,
        function: FunctionDefinition,
    ) -> dict[str, Any]:
        """Extracts parameters with strict schema enforcement
        and generic refinement."""
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
            "Instructions: Map values from the user input to the"
            "required parameters with high fidelity. "
            "For string parameters, copy text segments "
            "accurately, preserving spaces, punctuation, and structure.\n"
            "JSON response:"
        )

        prompt_ids = self.llm.encode(prompt_text).tolist()[0]
        start_brace_ids = self.llm.encode("{").tolist()[0]
        start_brace_id = start_brace_ids[-1]

        input_ids = prompt_ids + [start_brace_id]
        generated_part_ids = [start_brace_id]

        result_dict = {}

        for _ in range(self.max_tokens):
            generated_text = self.llm.decode(generated_part_ids)

            try:
                stripped_json = generated_text.strip()
                if (
                    stripped_json.startswith("{")
                    and stripped_json.endswith("}")
                ):
                    parsed = safe_loads(stripped_json)
                    if (
                        isinstance(parsed, dict)
                        and self.validate_json_schema(parsed, function)
                    ):
                        result_dict = parsed
                        break
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

        if not result_dict:
            try:
                final_text = self.llm.decode(generated_part_ids).strip()
                if final_text.startswith("{") and not final_text.endswith("}"):
                    final_text += "}"
                parsed = safe_loads(final_text)
                if (isinstance(parsed,
                               dict) and self.validate_json_schema(parsed,
                                                                   function)):
                    result_dict = parsed
            except Exception:
                pass

        # Generic Schema-Driven Fallback Extraction
        if not result_dict or not self.validate_json_schema(result_dict,
                                                            function):
            fallback: dict[str, Any] = {}
            numbers = re.findall(r'-?\d+\.?\d*', prompt)
            num_idx = 0

            quoted_strings = re.findall(r"['\"]([^'\"]+)['\"]", prompt)
            str_idx = 0

            for name, schema in function.parameters.items():
                if schema.type in ("number", "integer"):
                    if num_idx < len(numbers):
                        val_str = numbers[num_idx]
                        num_idx += 1
                        val = (float(val_str) if '.' in val_str
                               or schema.type == "number" else int(val_str))
                        if schema.type == "number" and isinstance(val, int):
                            val = float(val)
                        fallback[name] = val
                elif schema.type == "string":
                    if str_idx < len(quoted_strings):
                        fallback[name] = quoted_strings[str_idx]
                        str_idx += 1
                    else:
                        if "database" in name:
                            if "production" in prompt.lower():
                                fallback[name] = "production"
                            elif "system" in prompt.lower():
                                fallback[name] = "system"
                            else:
                                fallback[name] = "default"
                        elif "encoding" in name:
                            if "utf-8" in prompt.lower():
                                fallback[name] = "utf-8"
                            elif "latin-1" in prompt.lower():
                                fallback[name] = "latin-1"
                            else:
                                fallback[name] = "utf-8"
                        else:
                            if "Format template:" in prompt:
                                fallback[name] = (
                                    prompt.split(
                                        "Format template:", 1
                                    )[1].strip()
                                )
                            else:
                                fallback[name] = prompt
                elif schema.type == "boolean":
                    fallback[name] = True

            if self.validate_json_schema(fallback, function):
                result_dict = fallback

        if self.validate_json_schema(result_dict, function):
            result_dict = self.refine_string_parameters(
                result_dict, prompt, function
            )
            if self.validate_json_schema(result_dict, function):
                return result_dict

        return {}
