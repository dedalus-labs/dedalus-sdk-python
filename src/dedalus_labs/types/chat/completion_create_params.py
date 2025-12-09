# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..shared_params import mcp_servers as _mcp_servers
from .tool_choice_any_param import ToolChoiceAnyParam
from .tool_choice_auto_param import ToolChoiceAutoParam
from .tool_choice_none_param import ToolChoiceNoneParam
from .tool_choice_tool_param import ToolChoiceToolParam
from .prediction_content_param import PredictionContentParam
from .chat_completion_tool_param import ChatCompletionToolParam
from ..shared_params.dedalus_model import DedalusModel
from .thinking_config_enabled_param import ThinkingConfigEnabledParam
from ..shared_params.mcp_server_spec import MCPServerSpec
from .thinking_config_disabled_param import ThinkingConfigDisabledParam
from .chat_completion_functions_param import ChatCompletionFunctionsParam
from .chat_completion_tool_message_param import ChatCompletionToolMessageParam
from .chat_completion_user_message_param import ChatCompletionUserMessageParam
from ..shared_params.dedalus_model_choice import DedalusModelChoice
from ..shared_params.response_format_text import ResponseFormatText
from .chat_completion_system_message_param import ChatCompletionSystemMessageParam
from .chat_completion_function_message_param import ChatCompletionFunctionMessageParam
from .chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from .chat_completion_developer_message_param import ChatCompletionDeveloperMessageParam
from ..shared_params.response_format_json_object import ResponseFormatJSONObject
from ..shared_params.response_format_json_schema import ResponseFormatJSONSchema

__all__ = [
    "CompletionCreateParamsBase",
    "Model",
    "MCPServers",
    "Message",
    "ResponseFormat",
    "SafetySetting",
    "Thinking",
    "ToolChoice",
    "Tool",
    "ToolCustomToolChatCompletions",
    "ToolCustomToolChatCompletionsCustom",
    "ToolCustomToolChatCompletionsCustomFormat",
    "ToolCustomToolChatCompletionsCustomFormatTextFormat",
    "ToolCustomToolChatCompletionsCustomFormatGrammarFormat",
    "ToolCustomToolChatCompletionsCustomFormatGrammarFormatGrammar",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[Model]
    """Model identifier.

    Accepts model ID strings, lists for routing, or DedalusModel objects with
    per-model settings.
    """

    agent_attributes: Optional[Dict[str, float]]
    """Agent attributes. Values in [0.0, 1.0]."""

    audio: Optional[Dict[str, object]]
    """Parameters for audio output.

    Required when audio output is requested with `mo...
    """

    automatic_tool_execution: bool
    """Execute tools server-side.

    If false, returns raw tool calls for manual handling.
    """

    cached_content: Optional[str]
    """Optional.

    The name of the content [cached](https://ai.google.dev/gemini-api/d...
    """

    deferred: Optional[bool]
    """If set to `true`, the request returns a `request_id`.

    You can then get the de...
    """

    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on the...
    """

    function_call: Optional[str]
    """Wrapper for union variant: function call mode."""

    functions: Optional[Iterable[ChatCompletionFunctionsParam]]
    """Deprecated in favor of `tools`. A list of functions the model may generate J..."""

    generation_config: Optional[Dict[str, object]]
    """Generation parameters wrapper (Google-specific)"""

    guardrails: Optional[Iterable[Dict[str, object]]]
    """Content filtering and safety policy configuration."""

    handoff_config: Optional[Dict[str, object]]
    """Configuration for multi-model handoffs."""

    logit_bias: Optional[Dict[str, int]]
    """Modify the likelihood of specified tokens appearing in the completion. Accep..."""

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens or not.

    If true, ret...
    """

    max_completion_tokens: Optional[int]
    """Maximum tokens in completion (newer parameter name)"""

    max_tokens: Optional[int]
    """Maximum tokens in completion"""

    max_turns: Optional[int]
    """Maximum conversation turns."""

    mcp_servers: Optional[MCPServers]
    """MCP server identifiers.

    Accepts marketplace slugs, URLs, or MCPServerSpec objects. MCP tools are
    executed server-side and billed separately.
    """

    messages: Optional[Iterable[Message]]
    """Conversation history (OpenAI: messages, Google: contents, Responses: input)"""

    metadata: Optional[Dict[str, object]]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be usef...
    """

    modalities: Optional[SequenceNotStr[str]]
    """Output types that you would like the model to generate.

    Most models are capab...
    """

    model_attributes: Optional[Dict[str, Dict[str, float]]]
    """Model attributes for routing.

    Maps model IDs to attribute dictionaries with values in [0.0, 1.0].
    """

    n: Optional[int]
    """How many chat completion choices to generate for each input message.

    Note tha...
    """

    parallel_tool_calls: Optional[bool]
    """Whether to enable parallel tool calls (Anthropic uses inverted polarity)"""

    prediction: Optional[PredictionContentParam]
    """
    Static predicted output content, such as the content of a text file that is
    being regenerated.

    Fields:

    - type (required): Literal["content"]
    - content (required): str |
      Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
      ArrayTitle("PredictionContentArray")]
    """

    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whe...
    """

    prompt_cache_key: Optional[str]
    """
    Used by OpenAI to cache responses for similar requests to optimize your cache...
    """

    prompt_cache_retention: Optional[str]
    """The retention policy for the prompt cache.

    Set to `24h` to enable extended pr...
    """

    prompt_mode: Optional[Literal["reasoning"]]
    """Allows toggling between the reasoning mode and no system prompt.

    When set to ...
    """

    reasoning_effort: Optional[str]
    """
    Constrains effort on reasoning for [reasoning models](https://platform.openai...
    """

    response_format: Optional[ResponseFormat]
    """An object specifying the format that the model must output. Setting to `{ "..."""

    safe_prompt: Optional[bool]
    """Whether to inject a safety prompt before all conversations."""

    safety_identifier: Optional[str]
    """
    A stable identifier used to help detect users of your application that may be...
    """

    safety_settings: Optional[Iterable[SafetySetting]]
    """Safety/content filtering settings (Google-specific)"""

    search_parameters: Optional[Dict[str, object]]
    """Set the parameters to be used for searched data.

    If not set, no data will be ...
    """

    seed: Optional[int]
    """Random seed for deterministic output"""

    service_tier: Optional[str]
    """Service tier for request processing"""

    stop: Union[SequenceNotStr[str], str, None]
    """Sequences that stop generation"""

    store: Optional[bool]
    """
    Whether or not to store the output of this chat completion request for use in...
    """

    stream_options: Optional[Dict[str, object]]
    """Options for streaming response. Only set this when you set `stream: true`."""

    system_instruction: Union[Dict[str, object], str, None]
    """System instruction/prompt"""

    temperature: Optional[float]
    """Sampling temperature (0-2 for most providers)"""

    thinking: Optional[Thinking]
    """Extended thinking configuration (Anthropic-specific)"""

    tool_choice: Optional[ToolChoice]
    """Controls which (if any) tool is called by the model.

    `none` means the model w...
    """

    tool_config: Optional[Dict[str, object]]
    """Tool calling configuration (Google-specific)"""

    tools: Optional[Iterable[Tool]]
    """Available tools/functions for the model"""

    top_k: Optional[int]
    """Top-k sampling parameter"""

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying the number of most likely tokens to re...
    """

    top_p: Optional[float]
    """Nucleus sampling threshold"""

    user: Optional[str]
    """This field is being replaced by `safety_identifier` and `prompt_cache_key`.

    U...
    """

    verbosity: Optional[str]
    """Constrains the verbosity of the model's response.

    Lower values will result in...
    """

    web_search_options: Optional[Dict[str, object]]
    """This tool searches the web for relevant results to use in a response.

    Learn m...
    """


Model: TypeAlias = Union[str, DedalusModel, SequenceNotStr[DedalusModelChoice]]

MCPServers: TypeAlias = Union[str, MCPServerSpec, _mcp_servers.MCPServers]

Message: TypeAlias = Union[
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,
]

ResponseFormat: TypeAlias = Union[ResponseFormatText, ResponseFormatJSONSchema, ResponseFormatJSONObject]


class SafetySetting(TypedDict, total=False):
    """Safety setting, affecting the safety-blocking behavior.

    Passing a safety setting for a category changes the allowed probability that
    content is blocked.

    Fields:
    - category (required): HarmCategory
    - threshold (required): Literal["HARM_BLOCK_THRESHOLD_UNSPECIFIED", "BLOCK_LOW_AND_ABOVE", "BLOCK_MEDIUM_AND_ABOVE", "BLOCK_ONLY_HIGH", "BLOCK_NONE", "OFF"]
    """

    category: Required[
        Literal[
            "HARM_CATEGORY_UNSPECIFIED",
            "HARM_CATEGORY_DEROGATORY",
            "HARM_CATEGORY_TOXICITY",
            "HARM_CATEGORY_VIOLENCE",
            "HARM_CATEGORY_SEXUAL",
            "HARM_CATEGORY_MEDICAL",
            "HARM_CATEGORY_DANGEROUS",
            "HARM_CATEGORY_HARASSMENT",
            "HARM_CATEGORY_HATE_SPEECH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "HARM_CATEGORY_DANGEROUS_CONTENT",
            "HARM_CATEGORY_CIVIC_INTEGRITY",
        ]
    ]
    """Required. The category for this setting."""

    threshold: Required[
        Literal[
            "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
            "BLOCK_LOW_AND_ABOVE",
            "BLOCK_MEDIUM_AND_ABOVE",
            "BLOCK_ONLY_HIGH",
            "BLOCK_NONE",
            "OFF",
        ]
    ]
    """Required. Controls the probability threshold at which harm is blocked."""


Thinking: TypeAlias = Union[ThinkingConfigEnabledParam, ThinkingConfigDisabledParam]

ToolChoice: TypeAlias = Union[ToolChoiceAutoParam, ToolChoiceAnyParam, ToolChoiceToolParam, ToolChoiceNoneParam]


class ToolCustomToolChatCompletionsCustomFormatTextFormat(TypedDict, total=False):
    """Unconstrained free-form text.

    Fields:
    - type (required): Literal["text"]
    """

    type: Required[Literal["text"]]
    """Unconstrained text format. Always `text`."""


class ToolCustomToolChatCompletionsCustomFormatGrammarFormatGrammar(TypedDict, total=False):
    """Your chosen grammar."""

    definition: Required[str]
    """The grammar definition."""

    syntax: Required[Literal["lark", "regex"]]
    """The syntax of the grammar definition. One of `lark` or `regex`."""


class ToolCustomToolChatCompletionsCustomFormatGrammarFormat(TypedDict, total=False):
    """A grammar defined by the user.

    Fields:
    - type (required): Literal["grammar"]
    - grammar (required): GrammarFormatGrammarFormat
    """

    grammar: Required[ToolCustomToolChatCompletionsCustomFormatGrammarFormatGrammar]
    """Your chosen grammar."""

    type: Required[Literal["grammar"]]
    """Grammar format. Always `grammar`."""


ToolCustomToolChatCompletionsCustomFormat: TypeAlias = Union[
    ToolCustomToolChatCompletionsCustomFormatTextFormat, ToolCustomToolChatCompletionsCustomFormatGrammarFormat
]


class ToolCustomToolChatCompletionsCustom(TypedDict, total=False):
    """Properties of the custom tool."""

    name: Required[str]
    """The name of the custom tool, used to identify it in tool calls."""

    description: str
    """Optional description of the custom tool, used to provide more context."""

    format: ToolCustomToolChatCompletionsCustomFormat
    """The input format for the custom tool. Default is unconstrained text."""


class ToolCustomToolChatCompletions(TypedDict, total=False):
    """A custom tool that processes input using a specified format.

    Fields:
    - type (required): Literal["custom"]
    - custom (required): CustomToolProperties
    """

    custom: Required[ToolCustomToolChatCompletionsCustom]
    """Properties of the custom tool."""

    type: Required[Literal["custom"]]
    """The type of the custom tool. Always `custom`."""


Tool: TypeAlias = Union[ChatCompletionToolParam, ToolCustomToolChatCompletions]


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Optional[Literal[False]]
    """Enable streaming response"""


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Enable streaming response"""


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
