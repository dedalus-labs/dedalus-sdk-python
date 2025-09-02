# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from .model_id import ModelID
from .models_param import ModelsParam
from ..dedalus_model_param import DedalusModelParam

__all__ = [
    "CompletionCreateParamsBase",
    "Model",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    messages: Required[Iterable[Dict[str, object]]]
    """Messages to the model.

    Supports role/content structure and multimodal content arrays.
    """

    agent_attributes: Optional[Dict[str, float]]
    """Attributes for the agent itself, influencing behavior and model selection.

    Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
    'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
    values indicate stronger preference for that characteristic.
    """

    frequency_penalty: Optional[float]
    """Frequency penalty (-2 to 2).

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing likelihood of repeated phrases.
    """

    guardrails: Optional[Iterable[Dict[str, object]]]
    """Guardrails to apply to the agent for input/output validation and safety checks.

    Reserved for future use - guardrails configuration format not yet finalized.
    """

    handoff_config: Optional[Dict[str, object]]
    """Configuration for multi-model handoffs and agent orchestration.

    Reserved for future use - handoff configuration format not yet finalized.
    """

    logit_bias: Optional[Dict[str, int]]
    """Modify likelihood of specified tokens appearing in the completion.

    Maps token IDs (as strings) to bias values (-100 to 100). -100 = completely ban
    token, +100 = strongly favor token.
    """

    max_tokens: Optional[int]
    """Maximum number of tokens to generate in the completion.

    Does not include tokens in the input messages.
    """

    max_turns: Optional[int]
    """Maximum number of turns for agent execution before terminating (default: 10).

    Each turn represents one model inference cycle. Higher values allow more complex
    reasoning but increase cost and latency.
    """

    mcp_servers: Optional[SequenceNotStr[str]]
    """
    MCP (Model Context Protocol) server addresses to make available for server-side
    tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
    'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
    separately.
    """

    model: Optional[Model]
    """Model(s) to use for completion.

    Can be a single model ID, a DedalusModel object, or a list for multi-model
    routing. Single model: 'openai/gpt-4', 'anthropic/claude-3-5-sonnet-20241022',
    'openai/gpt-4o-mini', or a DedalusModel instance. Multi-model routing:
    ['openai/gpt-4o-mini', 'openai/gpt-4', 'anthropic/claude-3-5-sonnet'] or list of
    DedalusModel objects - agent will choose optimal model based on task complexity.
    """

    model_attributes: Optional[Dict[str, Dict[str, float]]]
    """
    Attributes for individual models used in routing decisions during multi-model
    execution. Format: {'model_name': {'attribute': value}}, where values are
    0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
    'accuracy'. Used by agent to select optimal model based on task requirements.
    """

    n: Optional[int]
    """Number of completions to generate. Note: only n=1 is currently supported."""

    presence_penalty: Optional[float]
    """Presence penalty (-2 to 2).

    Positive values penalize new tokens based on whether they appear in the text so
    far, encouraging the model to talk about new topics.
    """

    stop: Optional[SequenceNotStr[str]]
    """Up to 4 sequences where the API will stop generating further tokens.

    The model will stop as soon as it encounters any of these sequences.
    """

    temperature: Optional[float]
    """Sampling temperature (0 to 2).

    Higher values make output more random, lower values make it more focused and
    deterministic. 0 = deterministic, 1 = balanced, 2 = very creative.
    """

    tool_choice: Union[str, Dict[str, object], None]
    """Controls which tool is called by the model.

    Options: 'auto' (default), 'none', 'required', or specific tool name. Can also
    be a dict specifying a particular tool.
    """

    tools: Optional[Iterable[Dict[str, object]]]
    """list of tools available to the model in OpenAI function calling format.

    Tools are executed client-side and returned as JSON for the application to
    handle. Use 'mcp_servers' for server-side tool execution.
    """

    top_p: Optional[float]
    """Nucleus sampling parameter (0 to 1).

    Alternative to temperature. 0.1 = only top 10% probability mass, 1.0 = consider
    all tokens.
    """

    user: Optional[str]
    """Unique identifier representing your end-user.

    Used for monitoring and abuse detection. Should be consistent across requests
    from the same user.
    """


Model: TypeAlias = Union[ModelID, DedalusModelParam, ModelsParam]


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """Whether to stream back partial message deltas as Server-Sent Events.

    When true, partial message deltas will be sent as OpenAI-compatible chunks.
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether to stream back partial message deltas as Server-Sent Events.

    When true, partial message deltas will be sent as OpenAI-compatible chunks.
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
