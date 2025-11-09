from __future__ import annotations

from typing import Any, Dict, cast

import pydantic

from ._pydantic import to_strict_json_schema

__all__ = ["PydanticFunctionTool", "pydantic_function_tool"]


class PydanticFunctionTool(Dict[str, Any]):
    """Wrapper for Pydantic-based tool definitions.

    Preserves the Pydantic model through the request stack for argument parsing.
    """

    model: type[pydantic.BaseModel]

    def __init__(self, defn: Dict[str, Any], model: type[pydantic.BaseModel]) -> None:
        super().__init__(defn)
        self.model = model

    def cast(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], self)


def pydantic_function_tool(
    model: type[pydantic.BaseModel],
    *,
    name: str | None = None,
    description: str | None = None,
) -> Dict[str, Any]:
    """Create a function tool from a Pydantic model.

    Args:
        model: Pydantic BaseModel defining the tool's input schema
        name: Tool name (defaults to model class name)
        description: Tool description (defaults to model docstring)

    Returns:
        Tool definition dict compatible with chat.completions.create()
    """
    if description is None:
        description = model.__doc__

    function = PydanticFunctionTool(
        {
            "name": name or model.__name__,
            "strict": True,
            "parameters": to_strict_json_schema(model),
        },
        model,
    ).cast()

    if description is not None:
        function["description"] = description

    return {
        "type": "function",
        "function": function,
    }
