# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Union, Callable, Protocol
from typing_extensions import TypeAlias

__all__ = [
    "Tool",
    "ToolCall",
    "ToolResult",
    "ToolHandler",
    "JsonValue",
    "MCPToolResult",
]

JsonValue: TypeAlias = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

Tool = Callable[..., JsonValue]
ToolCall = Dict[str, Union[str, Dict[str, str]]]
ToolResult = Dict[str, Union[str, int, JsonValue]]


@dataclass
class MCPToolResult:
    """Result of an MCP tool execution from the API.

    Provides visibility into server-side MCP tool calls including
    the tool name, server name, input arguments, structured result,
    error status, and execution timing.
    """

    tool_name: str
    """Name of the MCP tool that was executed."""

    server_name: str
    """Name of the MCP server that handled the tool."""

    arguments: Dict[str, Any]
    """Input arguments passed to the tool."""

    result: Union[Dict[str, Any], List[Any], str, None]
    """Structured result from the tool."""

    is_error: bool
    """Whether the tool execution resulted in an error."""

    duration_ms: int | None = None
    """Execution time in milliseconds."""


class ToolHandler(Protocol):
    """Protocol for tool handlers."""
    def schemas(self) -> List[Dict[str, Any]]: ...
    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...
