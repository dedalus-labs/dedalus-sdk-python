# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import builtins
from typing import Dict, List, Optional
from typing_extensions import Literal

from .choice import Choice
from ..._models import BaseModel
from .completion_usage import CompletionUsage

__all__ = ["ChatCompletion"]


class ChatCompletion(BaseModel):
    """Chat completion response for Dedalus API.

    OpenAI-compatible chat completion response with Dedalus extensions.
    Maintains full compatibility with OpenAI API while providing additional
    features like server-side tool execution tracking and MCP error reporting.
    """

    id: str
    """A unique identifier for the chat completion."""

    choices: List[Choice]
    """A list of chat completion choices.

    Can be more than one if `n` is greater than 1.
    """

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created."""

    model: str
    """The model used for the chat completion."""

    object: Literal["chat.completion"]
    """The object type, which is always `chat.completion`."""

    mcp_server_errors: Optional[Dict[str, builtins.object]] = None
    """Information about MCP server failures, if any occurred during the request.

    Contains details about which servers failed and why, along with recommendations
    for the user. Only present when MCP server failures occurred.
    """

    mcp_tool_results: Optional[List["MCPToolResult"]] = None
    """Detailed results of MCP tool executions including inputs, outputs, and timing.

    Provides full visibility into server-side tool execution for debugging and audit
    purposes.
    """

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None
    """Specifies the processing type used for serving the request.

    - If set to 'auto', then the request will be processed with the service tier
      configured in the Project settings. Unless otherwise configured, the Project
      will use 'default'.
    - If set to 'default', then the request will be processed with the standard
      pricing and performance for the selected model.
    - If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or
      '[priority](https://openai.com/api-priority-processing/)', then the request
      will be processed with the corresponding service tier.
    - When not set, the default behavior is 'auto'.

    When the `service_tier` parameter is set, the response body will include the
    `service_tier` value based on the processing mode actually used to serve the
    request. This response value may be different from the value set in the
    parameter.
    """

    system_fingerprint: Optional[str] = None
    """This fingerprint represents the backend configuration that the model runs with.

    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """

    tools_executed: Optional[List[str]] = None
    """List of tool names that were executed server-side (e.g., MCP tools).

    Only present when tools were executed on the server rather than returned for
    client-side execution.
    """

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request."""


from ..shared.mcp_tool_result import MCPToolResult
