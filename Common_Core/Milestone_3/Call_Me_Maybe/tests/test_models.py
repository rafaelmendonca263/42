"""Unit tests for the Pydantic models."""

import pytest
from pydantic import ValidationError

from src.models import FunctionDefinition, FunctionParameterSchema


def test_function_definition_valid() -> None:
    """Test creating a valid FunctionDefinition."""
    func = FunctionDefinition(
        name="fn_add_numbers",
        description="Add two numbers.",
        parameters={
            "a": FunctionParameterSchema(type="number",
                                         description="First number"),
            "b": FunctionParameterSchema(type="number")
        },
        returns={"type": "number"}
    )

    assert func.name == "fn_add_numbers"
    assert "a" in func.parameters
    assert func.parameters["b"].type == "number"


def test_function_definition_missing_required_field() -> None:
    """Test that missing required fields raise a ValidationError."""
    with pytest.raises(ValidationError):
        # Intentionally passing incomplete arguments to trigger
        # Pydantic validation
        FunctionDefinition(
            description="This should fail."
        )  # type: ignore[call-arg]
