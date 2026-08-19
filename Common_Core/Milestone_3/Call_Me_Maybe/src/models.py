"""Modelos Pydantic para validação de dados de entrada e saída."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FunctionParameterSchema(BaseModel):
    """Esquema de um parâmetro de função."""

    type: str = Field(
        description="Tipo do parâmetro (number, string, boolean, etc.)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Descrição do parâmetro",
    )


class FunctionDefinition(BaseModel):
    """Definição de uma função disponível."""

    name: str = Field(description="Nome único da função")
    description: str = Field(description="Descrição do que a função faz")
    parameters: Dict[str, FunctionParameterSchema] = Field(
        default_factory=dict,
        description="Mapeamento de parâmetros esperados",
    )
    returns: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Tipo de retorno da função",
    )


class TestPrompt(BaseModel):
    """Estrutura do caso de teste de entrada."""

    prompt: str = Field(description="O pedido em linguagem natural")


class FunctionCallResult(BaseModel):
    """Estrutura do resultado exigida no output JSON."""

    prompt: str = Field(description="O pedido em linguagem natural original")
    name: str = Field(description="Nome da função selecionada")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Argumentos extraídos com tipos corretos",
    )
