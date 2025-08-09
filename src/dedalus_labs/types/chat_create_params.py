# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "ChatCreateParamsBase",
    "Model",
    "ModelModel",
    "ModelModelSettings",
    "ModelUnionMember3",
    "ModelUnionMember3Settings",
    "ChatCreateParamsNonStreaming",
    "ChatCreateParamsStreaming",
]


class ChatCreateParamsBase(TypedDict, total=False):
    agent_attributes: Optional[Dict[str, float]]
    """Attributes for the agent itself, influencing behavior and model selection."""

    frequency_penalty: Optional[float]
    """Frequency penalty (-2 to 2).

    Positive values penalize new tokens based on their existing frequency in the
    text so far.
    """

    input: Optional[Iterable[object]]
    """Input to the model - can be messages, images, or other modalities.

    Supports OpenAI chat format with role/content structure. For multimodal inputs,
    content can include text, images, or other media types.
    """

    logit_bias: Optional[Dict[str, int]]
    """Modify likelihood of specified tokens appearing in the completion."""

    max_tokens: Optional[int]
    """Maximum number of tokens to generate in the completion."""

    max_turns: Optional[int]
    """Maximum number of turns for agent execution before terminating (default: 10)."""

    mcp_servers: Optional[List[str]]
    """
    MCP (Model Context Protocol) server addresses to make available for server-side
    tool execution.
    """

    model: Optional[Model]
    """Model(s) to use for completion.

    Can be a single model ID, a Model object, or a list for multi-model routing.
    """

    model_attributes: Optional[Dict[str, Dict[str, float]]]
    """
    Attributes for individual models used in routing decisions during multi-model
    execution.
    """

    n: Optional[int]
    """Number of completions to generate. Note: only n=1 is currently supported."""

    presence_penalty: Optional[float]
    """Presence penalty (-2 to 2).

    Positive values penalize new tokens based on whether they appear in the text so
    far.
    """

    stop: Optional[List[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    temperature: Optional[float]
    """Sampling temperature (0 to 2).

    Higher values make output more random, lower values make it more focused and
    deterministic.
    """

    tool_choice: Union[str, object, None]
    """Controls which tool is called by the model."""

    tools: Optional[Iterable[object]]
    """List of tools available to the model in OpenAI function calling format."""

    top_p: Optional[float]
    """Nucleus sampling parameter (0 to 1). Alternative to temperature."""

    user: Optional[str]
    """Unique identifier representing your end-user."""


class ModelModelSettings(TypedDict, total=False):
    frequency_penalty: Optional[float]

    include_usage: Optional[bool]

    input_audio_format: Optional[str]

    max_tokens: Optional[int]

    metadata: Optional[Dict[str, str]]

    modalities: Optional[List[str]]

    output_audio_format: Optional[str]

    parallel_tool_calls: Optional[bool]

    presence_penalty: Optional[float]

    store: Optional[bool]

    temperature: Optional[float]

    top_p: Optional[float]

    voice: Optional[str]


class ModelModel(TypedDict, total=False):
    name: Required[str]
    """Model identifier (e.g., 'gpt-4', 'claude-3-5-sonnet')"""

    attributes: Optional[Dict[str, float]]
    """Model attributes as scores between 0-1. Used for multi-model routing decisions."""

    settings: Optional[ModelModelSettings]
    """
    Model generation settings including temperature, max_tokens, and other
    parameters.
    """


class ModelUnionMember3Settings(TypedDict, total=False):
    frequency_penalty: Optional[float]

    include_usage: Optional[bool]

    input_audio_format: Optional[str]

    max_tokens: Optional[int]

    metadata: Optional[Dict[str, str]]

    modalities: Optional[List[str]]

    output_audio_format: Optional[str]

    parallel_tool_calls: Optional[bool]

    presence_penalty: Optional[float]

    store: Optional[bool]

    temperature: Optional[float]

    top_p: Optional[float]

    voice: Optional[str]


class ModelUnionMember3(TypedDict, total=False):
    name: Required[str]
    """Model identifier (e.g., 'gpt-4', 'claude-3-5-sonnet')"""

    attributes: Optional[Dict[str, float]]
    """Model attributes as scores between 0-1. Used for multi-model routing decisions."""

    settings: Optional[ModelUnionMember3Settings]
    """
    Model generation settings including temperature, max_tokens, and other
    parameters.
    """


Model: TypeAlias = Union[str, List[str], ModelModel, Iterable[ModelUnionMember3]]


class ChatCreateParamsNonStreaming(ChatCreateParamsBase, total=False):
    stream: Optional[Literal[False]]
    """Whether to stream back partial message deltas as Server-Sent Events."""


class ChatCreateParamsStreaming(ChatCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether to stream back partial message deltas as Server-Sent Events."""


ChatCreateParams = Union[ChatCreateParamsNonStreaming, ChatCreateParamsStreaming]
