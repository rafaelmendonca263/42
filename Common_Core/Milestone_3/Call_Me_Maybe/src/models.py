from typing import Any, Dict
from pydantic import BaseModel


class ParameterSchema(BaseModel):
    type: str


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, ParameterSchema]
    returns: Dict[str, Any]


class TestInput(BaseModel):
    prompt: str
