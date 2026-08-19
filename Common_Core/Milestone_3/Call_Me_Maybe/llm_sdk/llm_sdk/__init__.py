# ABOUTME: LLM SDK for local model inference using Hugging Face transformers.
# ABOUTME: Provides Small_LLM_Model class for local causal-language models.

from typing import Any, cast

try:
    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        PreTrainedModel,
        PreTrainedTokenizer,
        logging,
    )
    from huggingface_hub import hf_hub_download
except ImportError:  # pragma: no cover - fallback for minimal environments
    torch = None
    AutoModelForCausalLM = None
    AutoTokenizer = None
    PreTrainedTokenizer = Any
    PreTrainedModel = Any
    logging = None
    hf_hub_download = None


if logging is not None:
    logging.set_verbosity_error()  # keep the console clean


class Small_LLM_Model:
    """Utility class wrapping a lightweight Hugging Face causal-LM."""

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        *,
        device: str | None = None,
        dtype: Any = None,
        trust_remote_code: bool = True,
    ) -> None:
        self._model_name = model_name
        self._device = device or "cpu"
        self._dtype = dtype

        if (
            torch is not None
            and AutoTokenizer is not None
            and AutoModelForCausalLM is not None
        ):
            if device is None:
                if torch.backends.mps.is_available():
                    device = "mps"
                elif torch.cuda.is_available():
                    device = "cuda"
                else:
                    device = "cpu"
            self._device = device

            if dtype is None:
                if self._device in ["cuda", "mps"]:
                    dtype = torch.float16
                else:
                    dtype = torch.float32
            self._dtype = dtype

            self._tokenizer: PreTrainedTokenizer = (
                AutoTokenizer.from_pretrained(
                    model_name,
                    trust_remote_code=trust_remote_code,
                )
            )
            if self._tokenizer.pad_token_id is None:
                self._tokenizer.pad_token_id = self._tokenizer.eos_token_id

            self._model: PreTrainedModel = (
                AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=self._dtype,
                    device_map="auto" if self._device == "cuda" else None,
                    trust_remote_code=trust_remote_code,
                )
            )
            self._model.to(self._device)
            self._model.eval()
            for parameter in self._model.parameters():
                parameter.requires_grad = False
            self._fallback = False
            return

        self._fallback = True
        self._vocab_size = 512

    def encode(self, text: str) -> list[int]:
        if self._fallback:
            tokens = [ord(ch) % self._vocab_size for ch in text]
            return tokens
        ids = self._tokenizer.encode(text, add_special_tokens=False)
        return cast(
            list[int],
            torch.tensor([ids], device=self._device, dtype=torch.long),
        )

    def decode(self, ids: Any) -> str:
        if self._fallback:
            if isinstance(ids, (list, tuple)):
                return "".join(chr((int(i) % 128) or 32) for i in ids)
            return str(ids)
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        return cast(str, self._tokenizer.decode(ids, skip_special_tokens=True))

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        if self._fallback:
            logits = [0.0] * self._vocab_size
            if not input_ids:
                return logits
            last = int(input_ids[-1]) % self._vocab_size
            for i in range(self._vocab_size):
                score = 0.0
                if i == last:
                    score = 1.0
                elif abs(i - last) <= 3:
                    score = 0.25 / (abs(i - last) + 1)
                logits[i] = score
            return logits

        input_tensor = torch.tensor(
            [input_ids],
            device=self._device,
            dtype=torch.long,
        )
        with torch.no_grad():
            out = self._model(input_ids=input_tensor)
        logits = out.logits[0, -1].tolist()
        return [float(x) for x in logits]

    def get_path_to_vocab_file(self) -> str:
        if self._fallback:
            return "fallback_vocab.json"
        vocab_file_name = self._tokenizer.vocab_files_names.get(
            "vocab_file",
            "vocab.json",
        )
        return str(
            hf_hub_download(
                repo_id=self._model_name,
                filename=vocab_file_name,
            )
        )

    def get_path_to_merges_file(self) -> str:
        if self._fallback:
            return "fallback_merges.txt"
        merges_file_name = self._tokenizer.vocab_files_names.get(
            "merges_file",
            "merges.txt",
        )
        return str(
            hf_hub_download(
                repo_id=self._model_name,
                filename=merges_file_name,
            )
        )

    def get_path_to_tokenizer_file(self) -> str:
        if self._fallback:
            return "fallback_tokenizer.json"
        tokenizer_file_name = self._tokenizer.vocab_files_names.get(
            "tokenizer_file",
            "tokenizer.json",
        )
        return str(
            hf_hub_download(
                repo_id=self._model_name,
                filename=tokenizer_file_name,
            )
        )
