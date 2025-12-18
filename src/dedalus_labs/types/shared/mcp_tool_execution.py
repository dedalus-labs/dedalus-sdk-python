# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

from ..._models import BaseModel

__all__ = ["MCPToolExecution"]


class MCPToolExecution(BaseModel):
    """Details of a single MCP tool execution.

    Provides visibility into MCP tool calls including the full input arguments
    and structured output, enabling debugging and audit trails.
    """

    server_name: str
    """Name of the MCP server that handled the tool"""

    tool_name: str
    """Name of the MCP tool that was executed"""

    arguments: Optional["JSONObjectOutput"] = None
    """Input arguments passed to the tool"""

    duration_ms: Optional[int] = None
    """Execution time in milliseconds"""

    is_error: Optional[bool] = None
    """Whether the tool execution resulted in an error"""

    result: Optional["JSONValueOutput"] = None
    """Structured result from the tool (parsed from structuredContent or content)"""


from .json_value_output import JSONValueOutput
from .json_object_output import JSONObjectOutput
