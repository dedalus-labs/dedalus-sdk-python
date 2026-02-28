# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal

from .choice import Choice
from ..._models import BaseModel
from .completion_usage import CompletionUsage

__all__ = ["ChatCompletion", "MCPServerErrors", "PendingTool"]


class MCPServerErrors(BaseModel):
    """Error details for a single MCP server failure."""

    message: str
    """Human-readable error message."""

    code: Optional[str] = None
    """Machine-readable error code."""

    recommendation: Optional[str] = None
    """Suggested action for the user."""


class PendingTool(BaseModel):
    """Client-side tool call the SDK must execute."""

    id: str
    """Unique identifier for this tool call."""

    arguments: "JSONObjectInput"
    """Input arguments for the tool call."""

    name: str
    """Name of the tool to execute."""

    dependencies: Optional[List[str]] = None
    """IDs of other pending calls that must complete first."""


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

    correlation_id: Optional[str] = None
    """Stable session ID for cross-turn handoff state.

    Echo this on the next request to resume server-side execution.
    """

    deferred: Optional[List["DeferredCallResponse"]] = None
    """Server tools blocked on client results."""

    mcp_server_errors: Optional[Dict[str, MCPServerErrors]] = None
    """MCP server failures keyed by server name."""

    mcp_tool_results: Optional[List["MCPToolResult"]] = None
    """Detailed results of MCP tool executions including inputs, outputs, and timing.

    Provides full visibility into server-side tool execution for debugging and audit
    purposes.
    """

    pending_tools: Optional[List[PendingTool]] = None
    """Client tools to execute, with dependency ordering."""

    server_results: Optional[Dict[str, Optional["JSONValueInput"]]] = None
    """Completed server tool outputs keyed by call ID."""

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None
    """Specifies the processing type used for serving the request.

    - If set to 'auto', then the request will be processed with the service tier
      configured in the Project settings. Unless otherwise configured, the Project
      will use 'default'.
    - If set to 'default', then the request will be processed with the standard
      pricing and performance for the selected model.
    - If set to '[flex](/docs/guides/flex-processing)' or
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

    turns_consumed: Optional[int] = None
    """Number of internal LLM calls made during this request.

    SDKs can sum this across their outer loop to track total LLM calls.
    """

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request."""


from .deferred_call_response import DeferredCallResponse
from ..shared.mcp_tool_result import MCPToolResult
from ..shared.json_value_input import JSONValueInput
from ..shared.json_object_input import JSONObjectInput
