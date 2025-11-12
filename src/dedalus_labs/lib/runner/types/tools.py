# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Any, Dict, List, Union, Callable, Protocol
from typing_extensions import TypeAlias

__all__ = [
    "Tool",
    "ToolCall",
    "ToolResult",
    "ToolHandler",
    "JsonValue",
]

JsonValue: TypeAlias = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

Tool = Callable[..., JsonValue]
ToolCall = Dict[str, Union[str, Dict[str, str]]]
ToolResult = Dict[str, Union[str, int, JsonValue]]


class ToolHandler(Protocol):
    """Protocol for tool handlers."""
    def schemas(self) -> List[Dict[str, Any]]: ...
    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...
