# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import inspect
from typing import Any, Callable

from pydantic import create_model

__all__ = [
    "to_schema",
]


def to_schema(func: Callable) -> dict[str, Any]:
    """Convert a Python function's signature to an OpenAPI-compatible JSON schema using Pydantic."""
    try:
        sig = inspect.signature(func)
        fields: dict[str, Any] = {}

        for name, param in sig.parameters.items():
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
            default = param.default if param.default != inspect.Parameter.empty else ...
            fields[name] = (annotation, default)

        if not fields:
            fields["input"] = (str, ...)

        DynamicModel = create_model(func.__name__, **fields)
        schema = DynamicModel.model_json_schema()

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or f"Execute {func.__name__}",
                "parameters": schema,
            },
        }
    except Exception:
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or f"Execute {func.__name__}",
                "parameters": {"type": "object", "properties": {}},
            },
        }
