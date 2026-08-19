"""Módulo para leitura, escrita e validação dos ficheiros JSON."""

import json
from pathlib import Path
from typing import List

from pydantic import ValidationError

from src.models import FunctionCallResult, FunctionDefinition, TestPrompt


def load_functions(file_path: str) -> List[FunctionDefinition]:
    """Carrega e valida as definições de funções a partir de um JSON."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Ficheiro de funções não encontrado em: {file_path}",
        )

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [FunctionDefinition(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as err:
        raise ValueError(
            f"Erro ao validar ficheiro de funções ({file_path}): {err}",
        ) from err


def load_test_prompts(file_path: str) -> List[TestPrompt]:
    """Carrega e valida os casos de teste a partir de um JSON."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Ficheiro de testes não encontrado em: {file_path}",
        )

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [TestPrompt(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as err:
        raise ValueError(
            f"Erro ao validar ficheiro de testes ({file_path}): {err}",
        ) from err


def save_results(file_path: str, results: List[FunctionCallResult]) -> None:
    """Guarda a lista de resultados no ficheiro JSON de saída."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = [res.model_dump() for res in results]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
