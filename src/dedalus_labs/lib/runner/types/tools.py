# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-labs-python-sdk/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Any, Callable, Protocol, TypeAlias

__all__ = [
    "Tool",
    "ToolCall",
    "ToolResult",
    "ToolHandler",
    "JsonValue",
]

JsonValue: TypeAlias = str | int | float | bool | None | dict[str, Any] | list[Any]

Tool = Callable[..., JsonValue]
ToolCall = dict[str, str | dict[str, str]]
ToolResult = dict[str, str | int | JsonValue]


class ToolHandler(Protocol):
    """Protocol for tool handlers."""
    def schemas(self) -> list[dict[str, Any]]: ...
    async def exec(self, name: str, args: dict[str, JsonValue]) -> JsonValue: ...