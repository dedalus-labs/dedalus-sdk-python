# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

from ..._models import BaseModel

__all__ = ["MCPToolResult"]


class MCPToolResult(BaseModel):
    """Result of a single MCP tool execution.

    Provides visibility into MCP tool calls including the full input arguments
    and structured output, enabling debugging and audit trails.
    """

    arguments: "JSONObjectInput"
    """Input arguments passed to the tool"""

    is_error: bool
    """Whether the tool execution resulted in an error"""

    server_name: str
    """Name of the MCP server that handled the tool"""

    tool_name: str
    """Name of the MCP tool that was executed"""

    duration_ms: Optional[int] = None
    """Execution time in milliseconds"""

    result: Optional["JSONValueInput"] = None
    """Structured result from the tool (parsed from structuredContent or content)"""


from .json_value_input import JSONValueInput
from .json_object_input import JSONObjectInput
