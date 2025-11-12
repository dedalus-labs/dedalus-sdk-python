# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from .model_id import ModelID
from .models_param import ModelsParam
from ..shared_params.dedalus_model import DedalusModel
from ..shared_params.response_format_text import ResponseFormatText
from ..shared_params.response_format_json_object import ResponseFormatJSONObject
from ..shared_params.response_format_json_schema import ResponseFormatJSONSchema

__all__ = [
    "CompletionCreateParamsBase",
    "Model",
    "ResponseFormat",
    "Thinking",
    "ThinkingThinkingConfigDisabled",
    "ThinkingThinkingConfigEnabled",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[Model]
    """Model(s) to use for completion.

    Can be a single model ID, a DedalusModel object, or a list for multi-model
    routing. Single model: 'openai/gpt-4', 'anthropic/claude-3-5-sonnet-20241022',
    'openai/gpt-4o-mini', or a DedalusModel instance. Multi-model routing:
    ['openai/gpt-4o-mini', 'openai/gpt-4', 'anthropic/claude-3-5-sonnet'] or list of
    DedalusModel objects - agent will choose optimal model based on task complexity.
    """

    agent_attributes: Optional[Dict[str, float]]
    """Attributes for the agent itself, influencing behavior and model selection.

    Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
    'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
    values indicate stronger preference for that characteristic.
    """

    audio: Optional[Dict[str, object]]
    """Parameters for audio output.

    Required when requesting audio responses (for example, modalities including
    'audio').
    """

    auto_execute_tools: bool
    """
    When False, skip server-side tool execution and return raw OpenAI-style
    tool_calls in the response.
    """

    deferred: Optional[bool]
    """xAI-specific parameter.

    If set to true, the request returns a request_id for async completion retrieval
    via GET /v1/chat/deferred-completion/{request_id}.
    """

    disable_automatic_function_calling: Optional[bool]
    """Google-only flag to disable the SDK's automatic function execution.

    When true, the model returns function calls for the client to execute manually.
    """

    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """

    function_call: Union[str, Dict[str, object], None]
    """Deprecated in favor of 'tool_choice'.

    Controls which function is called by the model (none, auto, or specific name).
    """

    functions: Optional[Iterable[Dict[str, object]]]
    """Deprecated in favor of 'tools'.

    Legacy list of function definitions the model may generate JSON inputs for.
    """

    generation_config: Optional[Dict[str, object]]
    """Google generationConfig object.

    Merged with auto-generated config. Use for Google-specific params
    (candidateCount, responseMimeType, etc.).
    """

    guardrails: Optional[Iterable[Dict[str, object]]]
    """Guardrails to apply to the agent for input/output validation and safety checks.

    Reserved for future use - guardrails configuration format not yet finalized.
    """

    handoff_config: Optional[Dict[str, object]]
    """Configuration for multi-model handoffs and agent orchestration.

    Reserved for future use - handoff configuration format not yet finalized.
    """

    input: Union[Iterable[Dict[str, object]], str, None]
    """Convenience alias for Responses-style `input`.

    Used when `messages` is omitted to provide the user prompt directly.
    """

    instructions: Union[str, Iterable[Dict[str, object]], None]
    """Convenience alias for Responses-style `instructions`.

    Takes precedence over `system` and over system-role messages when provided.
    """

    logit_bias: Optional[Dict[str, int]]
    """Modify the likelihood of specified tokens appearing in the completion.

    Accepts a JSON object mapping token IDs (as strings) to bias values from -100
    to 100. The bias is added to the logits before sampling; values between -1 and 1
    nudge selection probability, while values like -100 or 100 effectively ban or
    require a token.
    """

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens.

    If true, returns the log probabilities for each token in the response content.
    """

    max_completion_tokens: Optional[int]
    """
    An upper bound for the number of tokens that can be generated for a completion,
    including visible output and reasoning tokens.
    """

    max_tokens: Optional[int]
    """The maximum number of tokens that can be generated in the chat completion.

    This value can be used to control costs for text generated via API. This value
    is now deprecated in favor of 'max_completion_tokens' and is not compatible with
    o-series models.
    """

    max_turns: Optional[int]
    """Maximum number of turns for agent execution before terminating (default: 10).

    Each turn represents one model inference cycle. Higher values allow more complex
    reasoning but increase cost and latency.
    """

    mcp_servers: Union[str, SequenceNotStr[str], None]
    """
    MCP (Model Context Protocol) server addresses to make available for server-side
    tool execution. Entries can be URLs (e.g., 'https://mcp.example.com'), slugs
    (e.g., 'dedalus-labs/brave-search'), or structured objects specifying
    slug/version/url. MCP tools are executed server-side and billed separately.
    """

    messages: Union[Iterable[Dict[str, object]], str, None]
    """Conversation history.

    Accepts either a list of message objects or a string, which is treated as a
    single user message. Optional if `input` or `instructions` is provided.
    """

    metadata: Optional[Dict[str, str]]
    """
    Set of up to 16 key-value string pairs that can be attached to the request for
    structured metadata.
    """

    modalities: Optional[SequenceNotStr[str]]
    """Output types you would like the model to generate.

    Most models default to ['text']; some support ['text', 'audio'].
    """

    model_attributes: Optional[Dict[str, Dict[str, float]]]
    """
    Attributes for individual models used in routing decisions during multi-model
    execution. Format: {'model_name': {'attribute': value}}, where values are
    0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
    'accuracy'. Used by agent to select optimal model based on task requirements.
    """

    n: Optional[int]
    """How many chat completion choices to generate for each input message.

    Keep 'n' as 1 to minimize costs.
    """

    parallel_tool_calls: Optional[bool]
    """Whether to enable parallel function calling during tool use."""

    prediction: Optional[Dict[str, object]]
    """Configuration for predicted outputs.

    Improves response times when you already know large portions of the response
    content.
    """

    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whether they appear in the text so
    far, increasing the model's likelihood to talk about new topics.
    """

    prompt_cache_key: Optional[str]
    """
    Used by OpenAI to cache responses for similar requests and optimize cache hit
    rates. Replaces the legacy 'user' field for caching.
    """

    reasoning_effort: Optional[Literal["low", "medium", "high"]]
    """Constrains effort on reasoning for supported reasoning models.

    Higher values use more compute, potentially improving reasoning quality at the
    cost of latency and tokens.
    """

    response_format: Optional[ResponseFormat]
    """An object specifying the format that the model must output.

    Use {'type': 'json_schema', 'json_schema': {...}} for structured outputs or
    {'type': 'json_object'} for the legacy JSON mode. Currently only OpenAI-prefixed
    models honour this field; Anthropic and Google requests will return an
    invalid_request_error if it is supplied.
    """

    safety_identifier: Optional[str]
    """
    Stable identifier used to help detect users who might violate OpenAI usage
    policies. Consider hashing end-user identifiers before sending.
    """

    safety_settings: Optional[Iterable[Dict[str, object]]]
    """Google safety settings (harm categories and thresholds)."""

    search_parameters: Optional[Dict[str, object]]
    """xAI-specific parameter for configuring web search data acquisition.

    If not set, no data will be acquired by the model.
    """

    seed: Optional[int]
    """If specified, system will make a best effort to sample deterministically.

    Determinism is not guaranteed for the same seed across different models or API
    versions.
    """

    service_tier: Optional[Literal["auto", "default"]]
    """Specifies the processing tier used for the request.

    'auto' uses project defaults, while 'default' forces standard pricing and
    performance.
    """

    stop: Optional[SequenceNotStr[str]]
    """Not supported with latest reasoning models 'o3' and 'o4-mini'.

            Up to 4 sequences where the API will stop generating further tokens; the returned text will not contain the stop sequence.
    """

    store: Optional[bool]
    """
    Whether to store the output of this chat completion request for OpenAI model
    distillation or eval products. Image inputs over 8MB are dropped if storage is
    enabled.
    """

    stream_options: Optional[Dict[str, object]]
    """Options for streaming responses.

    Only set when 'stream' is true (supports 'include_usage' and
    'include_obfuscation').
    """

    system: Union[str, Iterable[Dict[str, object]], None]
    """System prompt/instructions.

    Anthropic: pass-through. Google: converted to systemInstruction. OpenAI:
    extracted from messages.
    """

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 make the output more random, while lower values like 0.2
    make it more focused and deterministic. We generally recommend altering this or
    'top_p' but not both.
    """

    thinking: Optional[Thinking]
    """Extended thinking configuration (Anthropic only).

    Enables thinking blocks showing reasoning process. Requires min 1,024 token
    budget.
    """

    tool_choice: Union[str, Dict[str, object], None]
    """Controls which (if any) tool is called by the model.

    'none' stops tool calling, 'auto' lets the model decide, and 'required' forces
    at least one tool invocation. Specific tool payloads force that tool.
    """

    tool_config: Optional[Dict[str, object]]
    """Google tool configuration (function calling mode, etc.)."""

    tools: Optional[Iterable[Dict[str, object]]]
    """A list of tools the model may call.

    Supports OpenAI function tools and custom tools; use 'mcp_servers' for
    Dedalus-managed server-side tools.
    """

    top_k: Optional[int]
    """Top-k sampling.

    Anthropic: pass-through. Google: injected into generationConfig.topK.
    """

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying how many of the most likely tokens to
    return at each position, with log probabilities. Requires 'logprobs' to be true.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered. We
    generally recommend altering this or 'temperature' but not both.
    """

    user: Optional[str]
    """Stable identifier for your end-users.

    Helps OpenAI detect and prevent abuse and may boost cache hit rates. This field
    is being replaced by 'safety_identifier' and 'prompt_cache_key'.
    """

    verbosity: Optional[Literal["low", "medium", "high"]]
    """Constrains the verbosity of the model's response.

    Lower values produce concise answers, higher values allow more detail.
    """

    web_search_options: Optional[Dict[str, object]]
    """Configuration for OpenAI's web search tool.

    Learn more at
    https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat.
    """


Model: TypeAlias = Union[ModelID, DedalusModel, ModelsParam]

ResponseFormat: TypeAlias = Union[ResponseFormatText, ResponseFormatJSONObject, ResponseFormatJSONSchema]


class ThinkingThinkingConfigDisabled(TypedDict, total=False):
    type: Required[Literal["disabled"]]


class ThinkingThinkingConfigEnabled(TypedDict, total=False):
    budget_tokens: Required[int]
    """Determines how many tokens Claude can use for its internal reasoning process.

    Larger budgets can enable more thorough analysis for complex problems, improving
    response quality.

    Must be ≥1024 and less than `max_tokens`.

    See
    [extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
    for details.
    """

    type: Required[Literal["enabled"]]


Thinking: TypeAlias = Union[ThinkingThinkingConfigDisabled, ThinkingThinkingConfigEnabled]


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """
    If true, the model response data is streamed to the client as it is generated
    using Server-Sent Events.
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """
    If true, the model response data is streamed to the client as it is generated
    using Server-Sent Events.
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
