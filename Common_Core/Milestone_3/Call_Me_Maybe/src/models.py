"""Pydantic models for validating input and output data."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FunctionParameterSchema(BaseModel):
    """Schema for a function parameter."""

    type: str = Field(
        description="Parameter type (number, string, boolean, etc.)",
    )
    description: Optional[str] = Field(
        default=None,
        description="Parameter description",
    )


class FunctionDefinition(BaseModel):
    """Definition of an available function."""

    name: str = Field(description="Unique function name")
    description: str = Field(description="What the function does")
    parameters: Dict[str, FunctionParameterSchema] = Field(
        default_factory=dict,
        description="Mapping of expected parameters",
    )
    returns: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Function return type",
    )


class TestPrompt(BaseModel):
    """Input test case structure."""

    prompt: str = Field(description="Natural-language request")


class FunctionCallResult(BaseModel):
    """Structure required in the JSON output."""

    prompt: str = Field(description="Original natural-language request")
    name: str = Field(description="Selected function name")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted arguments with correct types",
    )
