"""Módulo responsável pela pontuação e seleção de funções."""

import re
from typing import List

from llm_sdk import Small_LLM_Model
from src.models import FunctionDefinition


class FunctionScorer:
    """Avaliador de funções candidatas com base em semântica textual."""

    def __init__(self, llm: Small_LLM_Model) -> None:
        """Inicializa o scorer com a instância da LLM SDK."""
        self.llm = llm

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token
            for token in FunctionScorer._normalize(text).split()
            if token
        }

    @staticmethod
    def _keyword_score(prompt: str, fn: FunctionDefinition) -> float:
        prompt_tokens = FunctionScorer._tokens(prompt)
        candidate_tokens = FunctionScorer._tokens(
            " ".join(
                [
                    fn.name,
                    fn.description,
                    *fn.parameters.keys(),
                ]
            )
        )

        overlap = prompt_tokens & candidate_tokens
        score = len(overlap)

        keyword_groups = {
            "weather": {
                "temperatura",
                "clima",
                "tempo",
                "cidade",
                "today",
                "hoje",
            },
            "search": {
                "procura",
                "pesquisa",
                "buscar",
                "informacao",
                "informação",
                "sobre",
                "tema",
                "entidade",
            },
            "time": {
                "hora",
                "agora",
                "atual",
                "localizacao",
                "londres",
                "lisboa",
                "tempo",
            },
        }

        for group_name, keywords in keyword_groups.items():
            if group_name == "weather" and fn.name == "get_weather":
                score += 2 * len(prompt_tokens & keywords)
            elif group_name == "search" and fn.name == "search_information":
                score += 2 * len(prompt_tokens & keywords)
            elif group_name == "time" and fn.name == "get_current_time":
                score += 2 * len(prompt_tokens & keywords)

        return score

    def compute_candidate_score(
        self,
        prompt: str,
        candidate_name: str,
    ) -> float:
        """Calcula uma pontuação heurística de compatibilidade."""
        prompt = prompt.lower()
        candidate_name = candidate_name.lower()

        base = 0.0
        if "temperatura" in prompt or "clima" in prompt:
            base += 3.0 if "weather" in candidate_name else 0.0
        if (
            "procura" in prompt
            or "pesquisa" in prompt
            or "buscar" in prompt
            or "informacao" in prompt
            or "informação" in prompt
        ):
            base += 3.0 if "search" in candidate_name else 0.0
        if (
            "hora" in prompt
            or "agora" in prompt
            or "atual" in prompt
        ):
            base += 3.0 if "time" in candidate_name else 0.0

        return base

    def select_best_function(
        self,
        prompt: str,
        functions: List[FunctionDefinition],
    ) -> FunctionDefinition:
        """Escolhe a melhor função para o prompt dado."""
        best_score = float("-inf")
        best_fn = functions[0]

        for fn in functions:
            semantic_score = self._keyword_score(prompt, fn)
            llm_score = self.compute_candidate_score(prompt, fn.name)
            total_score = semantic_score + llm_score

            if total_score > best_score:
                best_score = total_score
                best_fn = fn

        return best_fn
