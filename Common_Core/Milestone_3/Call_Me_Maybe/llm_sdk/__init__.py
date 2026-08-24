"""Compatibility layer for the local llm_sdk package.

Allows importing the package directly from the repository.
"""

from .llm_sdk import Small_LLM_Model

__all__ = ["Small_LLM_Model"]
