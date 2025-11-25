# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from ..shared_params.dedalus_model import DedalusModel
from ..shared_params.dedalus_model_choice import DedalusModelChoice
from ..shared_params.response_format_text import ResponseFormatText
from ..shared_params.response_format_json_object import ResponseFormatJSONObject
from ..shared_params.response_format_json_schema import ResponseFormatJSONSchema

__all__ = [
    "CompletionCreateParamsBase",
    "Model",
    "Function",
    "MessagesMessage",
    "MessagesMessageChatCompletionRequestDeveloperMessage",
    "MessagesMessageChatCompletionRequestDeveloperMessageContentContent3",
    "MessagesMessageChatCompletionRequestSystemMessage",
    "MessagesMessageChatCompletionRequestSystemMessageContentContent4",
    "MessagesMessageChatCompletionRequestUserMessage",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartText",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImage",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImageImageURL",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudio",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudioInputAudio",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFile",
    "MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFileFile",
    "MessagesMessageChatCompletionRequestAssistantMessage",
    "MessagesMessageChatCompletionRequestAssistantMessageAudio",
    "MessagesMessageChatCompletionRequestAssistantMessageContentContent6",
    "MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartText",
    "MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartRefusal",
    "MessagesMessageChatCompletionRequestAssistantMessageFunctionCall",
    "MessagesMessageChatCompletionRequestAssistantMessageToolCall",
    "MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInput",
    "MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInputFunction",
    "MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInput",
    "MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInputCustom",
    "MessagesMessageChatCompletionRequestToolMessage",
    "MessagesMessageChatCompletionRequestToolMessageContentContent7",
    "MessagesMessageChatCompletionRequestFunctionMessage",
    "Prediction",
    "ResponseFormat",
    "SafetySetting",
    "Thinking",
    "ThinkingThinkingConfigEnabled",
    "ThinkingThinkingConfigDisabled",
    "ToolChoice",
    "ToolChoiceToolChoiceAuto",
    "ToolChoiceToolChoiceAny",
    "ToolChoiceToolChoiceTool",
    "ToolChoiceToolChoiceNone",
    "Tool",
    "ToolFunction",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[Model]
    """Model(s) to use for completion.

    Can be a single model ID, a DedalusModel object, or a list for multi-model
    routing. Single model: 'openai/gpt-5', 'anthropic/claude-sonnet-4-5-20250929',
    'google/gemini-3-pro-preview', or a DedalusModel instance. Multi-model routing:
    ['openai/gpt-5', 'anthropic/claude-sonnet-4-5-20250929',
    'google/gemini-3-pro-preview'] or list of DedalusModel objects - agent will
    choose optimal model based on task complexity.
    """

    agent_attributes: Optional[Dict[str, float]]
    """Attributes for the agent itself, influencing behavior and model selection.

    Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
    'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
    values indicate stronger preference for that characteristic.
    """

    audio: Optional[Dict[str, object]]
    """Parameters for audio output.

    Required when audio output is requested with `modalities: ["audio"]`.
    [Learn more](https://platform.openai.com/docs/guides/audio).
    """

    auto_execute_tools: bool
    """
    When False, skip server-side tool execution and return raw OpenAI-style
    tool_calls in the response.
    """

    cached_content: Annotated[Optional[str], PropertyInfo(alias="cachedContent")]
    """Optional.

    The name of the content [cached](https://ai.google.dev/gemini-api/docs/caching)
    to use as context to serve the prediction. Format:
    `cachedContents/{cachedContent}`
    """

    deferred: Optional[bool]
    """If set to `true`, the request returns a `request_id`.

    You can then get the deferred response by GET
    `/v1/chat/deferred-completion/{request_id}`.
    """

    disable_automatic_function_calling: bool
    """Google SDK control: disable automatic function calling.

    Agent workflows handle tools manually.
    """

    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """

    function_call: Optional[Literal["auto", "none"]]
    """Deprecated in favor of `tool_choice`.

    Controls which (if any) function is called by the model. `none` means the model
    will not call a function and instead generates a message. `auto` means the model
    can pick between generating a message or calling a function. Specifying a
    particular function via `{"name": "my_function"}` forces the model to call that
    function. `none` is the default when no functions are present. `auto` is the
    default if functions are present.
    """

    functions: Optional[Iterable[Function]]
    """Deprecated in favor of `tools`.

    A list of functions the model may generate JSON inputs for.
    """

    generation_config: Optional[Dict[str, object]]
    """Generation parameters wrapper (Google-specific)"""

    guardrails: Optional[Iterable[Dict[str, object]]]
    """Guardrails to apply to the agent for input/output validation and safety checks.

    Reserved for future use - guardrails configuration format not yet finalized.
    """

    handoff_config: Optional[Dict[str, object]]
    """Configuration for multi-model handoffs and agent orchestration.

    Reserved for future use - handoff configuration format not yet finalized.
    """

    logit_bias: Optional[Dict[str, int]]
    """Modify the likelihood of specified tokens appearing in the completion.

    Accepts a JSON object that maps tokens (specified by their token ID in the
    tokenizer) to an associated bias value from -100 to 100. Mathematically, the
    bias is added to the logits generated by the model prior to sampling. The exact
    effect will vary per model, but values between -1 and 1 should decrease or
    increase likelihood of selection; values like -100 or 100 should result in a ban
    or exclusive selection of the relevant token.
    """

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens or not.

    If true, returns the log probabilities of each output token returned in the
    `content` of `message`.
    """

    max_completion_tokens: Optional[int]
    """
    An upper bound for the number of tokens that can be generated for a completion,
    including visible output and reasoning tokens.
    """

    max_tokens: Optional[int]
    """Maximum number of tokens the model can generate in the completion.

    The total token count (input + output) is limited by the model's context window.
    Setting this prevents unexpectedly long responses and helps control costs. For
    newer OpenAI models, use max_completion_tokens instead (more precise
    accounting). For other providers, max_tokens remains the standard parameter
    name.
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

    messages: Union[Iterable[MessagesMessage], str, None]
    """Conversation history.

    Accepts either a list of message objects or a string, which is treated as a
    single user message. Optional if `input` or `instructions` is provided.
    """

    metadata: Optional[Dict[str, str]]
    """Set of 16 key-value pairs that can be attached to an object.

    This can be useful for storing additional information about the object in a
    structured format, and querying for objects via API or the dashboard. Keys are
    strings with a maximum length of 64 characters. Values are strings with a
    maximum length of 512 characters.
    """

    modalities: Optional[List[Literal["text", "audio"]]]
    """Output modalities.

    Most models generate text by default. Use ['text', 'audio'] for audio-capable
    models.
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

    Note that you will be charged based on the number of generated tokens across all
    of the choices. Keep `n` as `1` to minimize costs.
    """

    parallel_tool_calls: Optional[bool]
    """Whether to enable parallel tool calls (Anthropic uses inverted polarity)"""

    prediction: Optional[Prediction]
    """
    Static predicted output content, such as the content of a text file that is
    being regenerated.
    """

    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whether they appear in the text so
    far, increasing the model's likelihood to talk about new topics.
    """

    prompt_cache_key: Optional[str]
    """
    Used by OpenAI to cache responses for similar requests to optimize your cache
    hit rates. Replaces the `user` field.
    [Learn more](https://platform.openai.com/docs/guides/prompt-caching).
    """

    prompt_cache_retention: Optional[Literal["24h", "in-memory"]]
    """The retention policy for the prompt cache.

    Set to `24h` to enable extended prompt caching, which keeps cached prefixes
    active for longer, up to a maximum of 24 hours.
    [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).
    """

    prompt_mode: Optional[Dict[str, object]]
    """Allows toggling between the reasoning mode and no system prompt.

    When set to `reasoning` the system prompt for reasoning models will be used.
    """

    reasoning_effort: Optional[Literal["high", "low", "medium", "minimal", "none"]]
    """
    Constrains effort on reasoning for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
    supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
    reasoning effort can result in faster responses and fewer tokens used on
    reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
    reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
    `medium`, and `high`. Tool calls are supported for all reasoning values in
    gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
    do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
    `high` reasoning effort.
    """

    response_format: Optional[ResponseFormat]
    """An object specifying the format that the model must output.

    Setting to `{ "type": "json_schema", "json_schema": {...} }` enables Structured
    Outputs which ensures the model will match your supplied JSON schema. Learn more
    in the
    [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
    Setting to `{ "type": "json_object" }` enables the older JSON mode, which
    ensures the message the model generates is valid JSON. Using `json_schema` is
    preferred for models that support it.
    """

    safe_prompt: Optional[bool]
    """Whether to inject a safety prompt before all conversations."""

    safety_identifier: Optional[str]
    """
    A stable identifier used to help detect users of your application that may be
    violating OpenAI's usage policies. The IDs should be a string that uniquely
    identifies each user. We recommend hashing their username or email address, in
    order to avoid sending us any identifying information.
    [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).
    """

    safety_settings: Optional[Iterable[SafetySetting]]
    """Safety/content filtering settings (Google-specific)"""

    search_parameters: Optional[Dict[str, object]]
    """Set the parameters to be used for searched data.

    If not set, no data will be acquired by the model.
    """

    seed: Optional[int]
    """Random seed for deterministic output"""

    service_tier: Optional[Literal["auto", "default", "flex", "priority", "scale", "standard_only"]]
    """Service tier for request processing"""

    stop: Union[str, SequenceNotStr[str], None]
    """Not supported with latest reasoning models 'o3' and 'o4-mini'.

    Up to 4 sequences where the API will stop generating further tokens; the
    returned text will not contain the stop sequence.
    """

    store: Optional[bool]
    """
    Whether or not to store the output of this chat completion request for use in
    our [model distillation](https://platform.openai.com/docs/guides/distillation)
    or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
    text and image inputs. Note: image inputs over 8MB will be dropped.
    """

    stream_options: Optional[Dict[str, object]]
    """Options for streaming response. Only set this when you set `stream: true`."""

    system_instruction: Union[Dict[str, object], str, None]
    """
    System-level instructions defining the assistant's behavior, role, and
    constraints. Sets the context and personality for the entire conversation.
    Different from user/assistant messages as it provides meta-instructions about
    how to respond rather than conversation content. OpenAI: Provided as system role
    message in messages array. Google: Top-level systemInstruction field (adapter
    extracts from messages). Anthropic: Top-level system parameter (adapter extracts
    from messages). Accepts both string and structured object formats depending on
    provider capabilities.
    """

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic. We generally recommend altering
    this or top_p but not both.
    """

    thinking: Optional[Thinking]
    """Extended thinking configuration (Anthropic-specific)"""

    tool_choice: Optional[ToolChoice]
    """Controls which (if any) tool is called by the model.

    `none` means the model will not call any tool and instead generates a message.
    `auto` means the model can pick between generating a message or calling one or
    more tools. `required` means the model must call one or more tools. Specifying a
    particular tool via `{"type": "function", "function": {"name": "my_function"}}`
    forces the model to call that tool. `none` is the default when no tools are
    present. `auto` is the default if tools are present.
    """

    tool_config: Optional[Dict[str, object]]
    """Tool calling configuration (Google-specific)"""

    tools: Optional[Iterable[Tool]]
    """A list of tools the model may call.

    You can provide either custom tools or function tools. All providers support
    tools. Adapters handle translation to provider-specific formats.
    """

    top_k: Optional[int]
    """Top-k sampling parameter limiting token selection to k most likely candidates.

    Only considers the top k highest probability tokens at each generation step,
    setting all other tokens' probabilities to zero. Reduces tail probability mass.
    Helps prevent selection of highly unlikely tokens, improving output coherence.
    Supported by Google and Anthropic; not available in OpenAI's API.
    """

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying the number of most likely tokens to
    return at each token position, each with an associated log probability.
    `logprobs` must be set to `true` if this parameter is used.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered. We
    generally recommend altering this or temperature but not both.
    """

    user: Optional[str]
    """This field is being replaced by `safety_identifier` and `prompt_cache_key`.

    Use `prompt_cache_key` instead to maintain caching optimizations. A stable
    identifier for your end-users. Used to boost cache hit rates by better bucketing
    similar requests and to help OpenAI detect and prevent abuse.
    [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).
    """

    verbosity: Optional[Literal["high", "low", "medium"]]
    """Constrains the verbosity of the model's response.

    Lower values will result in more concise responses, while higher values will
    result in more verbose responses. Currently supported values are `low`,
    `medium`, and `high`.
    """

    web_search_options: Optional[Dict[str, object]]
    """This tool searches the web for relevant results to use in a response.

    Learn more about the
    [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).
    """


Model: TypeAlias = Union[str, DedalusModel, SequenceNotStr[DedalusModelChoice]]


class Function(TypedDict, total=False):
    name: Required[str]
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: Dict[str, object]
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](https://platform.openai.com/docs/guides/function-calling) for
    examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """


class MessagesMessageChatCompletionRequestDeveloperMessageContentContent3(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestDeveloperMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessagesMessageChatCompletionRequestDeveloperMessageContentContent3]]]
    """The contents of the developer message."""

    role: Required[Literal["developer"]]
    """The role of the messages author, in this case `developer`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessagesMessageChatCompletionRequestSystemMessageContentContent4(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestSystemMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessagesMessageChatCompletionRequestSystemMessageContentContent4]]]
    """The contents of the system message."""

    role: Required[Literal["system"]]
    """The role of the messages author, in this case `system`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartText(
    TypedDict, total=False
):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImageImageURL(
    TypedDict, total=False
):
    url: Required[str]
    """Either a URL of the image or the base64 encoded image data."""

    detail: Literal["auto", "low", "high"]
    """Specifies the detail level of the image.

    Learn more in the
    [Vision guide](https://platform.openai.com/docs/guides/vision#low-or-high-fidelity-image-understanding).
    """


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImage(
    TypedDict, total=False
):
    image_url: Required[
        MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImageImageURL
    ]
    """Fields:

    - url (required): AnyUrl
    - detail (optional): Literal['auto', 'low', 'high']
    """

    type: Required[Literal["image_url"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudioInputAudio(
    TypedDict, total=False
):
    data: Required[str]
    """Base64 encoded audio data."""

    format: Required[Literal["wav", "mp3"]]
    """The format of the encoded audio data. Currently supports "wav" and "mp3"."""


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudio(
    TypedDict, total=False
):
    input_audio: Required[
        MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudioInputAudio
    ]
    """Fields:

    - data (required): str
    - format (required): Literal['wav', 'mp3']
    """

    type: Required[Literal["input_audio"]]
    """The type of the content part. Always `input_audio`."""


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFileFile(
    TypedDict, total=False
):
    file_data: str
    """
    The base64 encoded file data, used when passing the file to the model as a
    string.
    """

    file_id: str
    """The ID of an uploaded file to use as input."""

    filename: str
    """The name of the file, used when passing the file to the model as a string."""


class MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFile(
    TypedDict, total=False
):
    file: Required[
        MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFileFile
    ]
    """Fields:

    - filename (optional): str
    - file_data (optional): str
    - file_id (optional): str
    """

    type: Required[Literal["file"]]
    """The type of the content part. Always `file`."""


MessagesMessageChatCompletionRequestUserMessageContentContent5: TypeAlias = Union[
    MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartText,
    MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartImage,
    MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartAudio,
    MessagesMessageChatCompletionRequestUserMessageContentContent5ChatCompletionRequestMessageContentPartFile,
]


class MessagesMessageChatCompletionRequestUserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessagesMessageChatCompletionRequestUserMessageContentContent5]]]
    """The contents of the user message."""

    role: Required[Literal["user"]]
    """The role of the messages author, in this case `user`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessagesMessageChatCompletionRequestAssistantMessageAudio(TypedDict, total=False):
    id: Required[str]
    """Unique identifier for a previous audio response from the model."""


class MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartText(
    TypedDict, total=False
):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartRefusal(
    TypedDict, total=False
):
    refusal: Required[str]
    """The refusal message generated by the model."""

    type: Required[Literal["refusal"]]
    """The type of the content part."""


MessagesMessageChatCompletionRequestAssistantMessageContentContent6: TypeAlias = Union[
    MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartText,
    MessagesMessageChatCompletionRequestAssistantMessageContentContent6ChatCompletionRequestMessageContentPartRefusal,
]


class MessagesMessageChatCompletionRequestAssistantMessageFunctionCall(TypedDict, total=False):
    arguments: Required[str]
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Required[str]
    """The name of the function to call."""


class MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInputFunction(
    TypedDict, total=False
):
    arguments: Required[str]
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Required[str]
    """The name of the function to call."""


class MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInput(
    TypedDict, total=False
):
    id: Required[str]
    """The ID of the tool call."""

    function: Required[
        MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInputFunction
    ]
    """The function that the model called."""

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


class MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInputCustom(
    TypedDict, total=False
):
    input: Required[str]
    """The input for the custom tool call generated by the model."""

    name: Required[str]
    """The name of the custom tool to call."""


class MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInput(
    TypedDict, total=False
):
    id: Required[str]
    """The ID of the tool call."""

    custom: Required[
        MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInputCustom
    ]
    """The custom tool that the model called."""

    type: Required[Literal["custom"]]
    """The type of the tool. Always `custom`."""


MessagesMessageChatCompletionRequestAssistantMessageToolCall: TypeAlias = Union[
    MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageToolCallInput,
    MessagesMessageChatCompletionRequestAssistantMessageToolCallChatCompletionMessageCustomToolCallInput,
]


class MessagesMessageChatCompletionRequestAssistantMessage(TypedDict, total=False):
    role: Required[Literal["assistant"]]
    """The role of the messages author, in this case `assistant`."""

    audio: Optional[MessagesMessageChatCompletionRequestAssistantMessageAudio]
    """Data about a previous audio response from the model.

    [Learn more](https://platform.openai.com/docs/guides/audio).

    Fields:

    - id (required): str
    """

    content: Union[str, Iterable[MessagesMessageChatCompletionRequestAssistantMessageContentContent6], None]
    """The contents of the assistant message.

    Required unless `tool_calls` or `function_call` is specified.
    """

    function_call: Optional[MessagesMessageChatCompletionRequestAssistantMessageFunctionCall]
    """Deprecated and replaced by `tool_calls`.

    The name and arguments of a function that should be called, as generated by the
    model.

    Fields:

    - arguments (required): str
    - name (required): str
    """

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """

    refusal: Optional[str]
    """The refusal message by the assistant."""

    tool_calls: Iterable[MessagesMessageChatCompletionRequestAssistantMessageToolCall]
    """The tool calls generated by the model, such as function calls."""


class MessagesMessageChatCompletionRequestToolMessageContentContent7(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessagesMessageChatCompletionRequestToolMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessagesMessageChatCompletionRequestToolMessageContentContent7]]]
    """The contents of the tool message."""

    role: Required[Literal["tool"]]
    """The role of the messages author, in this case `tool`."""

    tool_call_id: Required[str]
    """Tool call that this message is responding to."""


class MessagesMessageChatCompletionRequestFunctionMessage(TypedDict, total=False):
    content: Required[Optional[str]]
    """The contents of the function message."""

    name: Required[str]
    """The name of the function to call."""

    role: Required[Literal["function"]]
    """The role of the messages author, in this case `function`."""


MessagesMessage: TypeAlias = Union[
    MessagesMessageChatCompletionRequestDeveloperMessage,
    MessagesMessageChatCompletionRequestSystemMessage,
    MessagesMessageChatCompletionRequestUserMessage,
    MessagesMessageChatCompletionRequestAssistantMessage,
    MessagesMessageChatCompletionRequestToolMessage,
    MessagesMessageChatCompletionRequestFunctionMessage,
]


class Prediction(TypedDict, total=False):
    content: Required[Dict[str, object]]

    type: Literal["content"]


ResponseFormat: TypeAlias = Union[ResponseFormatText, ResponseFormatJSONSchema, ResponseFormatJSONObject]


class SafetySetting(TypedDict, total=False):
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


class ThinkingThinkingConfigEnabled(TypedDict, total=False):
    budget_tokens: Required[int]

    type: Literal["enabled"]


class ThinkingThinkingConfigDisabled(TypedDict, total=False):
    type: Literal["disabled"]


Thinking: TypeAlias = Union[ThinkingThinkingConfigEnabled, ThinkingThinkingConfigDisabled]


class ToolChoiceToolChoiceAuto(TypedDict, total=False):
    disable_parallel_tool_use: Optional[bool]

    type: Literal["auto"]


class ToolChoiceToolChoiceAny(TypedDict, total=False):
    disable_parallel_tool_use: Optional[bool]

    type: Literal["any"]


class ToolChoiceToolChoiceTool(TypedDict, total=False):
    name: Required[str]

    disable_parallel_tool_use: Optional[bool]

    type: Literal["tool"]


class ToolChoiceToolChoiceNone(TypedDict, total=False):
    type: Literal["none"]


ToolChoice: TypeAlias = Union[
    ToolChoiceToolChoiceAuto, ToolChoiceToolChoiceAny, ToolChoiceToolChoiceTool, ToolChoiceToolChoiceNone
]


class ToolFunction(TypedDict, total=False):
    name: Required[str]
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: Dict[str, object]
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](https://platform.openai.com/docs/guides/function-calling) for
    examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """

    strict: Optional[bool]
    """Whether to enable strict schema adherence when generating the function call.

    If set to true, the model will follow the exact schema defined in the
    `parameters` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. Learn more about Structured Outputs in the
    [function calling guide](https://platform.openai.com/docs/guides/function-calling).
    """


class Tool(TypedDict, total=False):
    function: Required[ToolFunction]
    """Fields:

    - description (optional): str
    - name (required): str
    - parameters (optional): FunctionParameters
    - strict (optional): bool | None
    """

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Optional[Literal[False]]
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
