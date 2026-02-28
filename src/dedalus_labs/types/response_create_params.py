# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .shared_params import mcp_servers
from .shared_params.credential import Credential
from .shared_params.mcp_credentials import MCPCredentials
from .shared_params.mcp_server_spec import MCPServerSpec

__all__ = [
    "ResponseCreateParams",
    "Conversation",
    "ConversationResponseConversationParam",
    "Credentials",
    "MCPServers",
    "Model",
    "Prompt",
]


class ResponseCreateParams(TypedDict, total=False):
    background: Optional[bool]
    """
    Whether to run the model response in the background.
    [Learn more](https://platform.openai.com/docs/guides/background).
    """

    conversation: Optional[Conversation]
    """Conversation that this response belongs to.

    Items from this conversation are prepended to the input items, and output items
    from this response are automatically added after completion.
    """

    credentials: Optional[Credentials]
    """Credentials for MCP server authentication.

    Each credential is matched to servers by connection name.
    """

    frequency_penalty: Optional[float]
    """Penalizes new tokens based on their frequency in the text so far."""

    include: Optional[SequenceNotStr[str]]
    """Specify additional output data to include in the model response.

    Currently supported values are:

    - `web_search_call.action.sources`: Include the sources of the web search tool
      call.
    - `code_interpreter_call.outputs`: Includes the outputs of python code execution
      in code interpreter tool call items.
    - `computer_call_output.output.image_url`: Include image urls from the computer
      call output.
    - `file_search_call.results`: Include the search results of the file search tool
      call.
    - `message.input_image.image_url`: Include image urls from the input message.
    - `message.output_text.logprobs`: Include logprobs with assistant messages.
    - `reasoning.encrypted_content`: Includes an encrypted version of reasoning
      tokens in reasoning item outputs. This enables reasoning items to be used in
      multi-turn conversations when using the Responses API statelessly (like when
      the `store` parameter is set to `false`, or when an organization is enrolled
      in the zero data retention program).
    """

    input: Union[str, Iterable["JSONObjectInput"], None]
    """Text, image, or file inputs to the model, used to generate a response.

    Learn more:

    - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
    - [Image inputs](https://platform.openai.com/docs/guides/images)
    - [File inputs](https://platform.openai.com/docs/guides/pdf-files)
    - [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
    - [Function calling](https://platform.openai.com/docs/guides/function-calling)
    """

    instructions: Union[str, Iterable["JSONObjectInput"], None]
    """A system (or developer) message inserted into the model's context.

    When using along with `previous_response_id`, the instructions from a previous
    response will not be carried over to the next response. This makes it simple to
    swap out system (or developer) messages in new responses.
    """

    max_output_tokens: Optional[int]
    """
    An upper bound for the number of tokens that can be generated for a response,
    including visible output tokens and
    [reasoning tokens](https://platform.openai.com/docs/guides/reasoning).
    """

    max_tool_calls: Optional[int]
    """
    The maximum number of total calls to built-in tools that can be processed in a
    response. This maximum number applies across all built-in tool calls, not per
    individual tool. Any further attempts to call a tool by the model will be
    ignored.
    """

    mcp_servers: Optional[MCPServers]
    """MCP server identifiers.

    Accepts marketplace slugs, URLs, or MCPServerSpec objects. MCP tools are
    executed server-side and billed separately.
    """

    metadata: Optional[Dict[str, str]]
    """
    Set of up to 16 key-value string pairs that can be attached to the response for
    structured metadata and later querying via the API or dashboard.
    """

    model: Optional[Model]
    """Model ID used to generate the response, like `gpt-4o` or `o3`.

    OpenAI offers a wide range of models with different capabilities, performance
    characteristics, and price points. Refer to the
    [model guide](https://platform.openai.com/docs/models) to browse and compare
    available models.
    """

    parallel_tool_calls: Optional[bool]
    """Whether to allow the model to run tool calls in parallel."""

    presence_penalty: Optional[float]
    """Penalizes new tokens based on whether they appear in the text so far."""

    previous_response_id: Optional[str]
    """
    Unique ID of the previous response to continue from when creating multi-turn
    conversations. Cannot be used together with `conversation`.
    """

    prompt: Optional[Prompt]
    """Stored prompt template reference (BYOK)."""

    prompt_cache_key: Optional[str]
    """
    Used by OpenAI to cache responses for similar requests to optimize your cache
    hit rates. Replaces the `user` field.
    [Learn more](https://platform.openai.com/docs/guides/prompt-caching).
    """

    reasoning: Optional["JSONObjectInput"]
    """**gpt-5 and o-series models only**

    Configuration options for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    """

    safety_identifier: Optional[str]
    """
    A stable identifier used to help detect users of your application that may be
    violating OpenAI's usage policies. The IDs should be a string that uniquely
    identifies each user. We recommend hashing their username or email address, in
    order to avoid sending us any identifying information.
    [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).
    """

    service_tier: Optional[Literal["auto", "default"]]
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

    store: Optional[bool]
    """
    Whether to store the generated response for later retrieval via the Responses
    API.
    """

    stream: bool
    """
    If set to true, the model response data will be streamed to the client as it is
    generated using
    [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format).
    See the
    [Streaming section below](https://platform.openai.com/docs/api-reference/responses-streaming)
    for more information.
    """

    stream_options: Optional["JSONObjectInput"]
    """Options for streaming response. Only set this when you set `stream: true`."""

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic. We generally recommend altering
    this or `top_p` but not both.
    """

    text: Optional["JSONObjectInput"]
    """Configuration options for a text response from the model.

    Can be plain text or structured JSON data. Learn more:

    - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
    - [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
    """

    tool_choice: Union[str, "JSONObjectInput", None]
    """
    How the model should select which tool (or tools) to use when generating a
    response. See the `tools` parameter to see how to specify which tools the model
    can call.
    """

    tools: Optional[Iterable["JSONObjectInput"]]
    """An array of tools the model may call while generating a response.

    You can specify which tool to use by setting the `tool_choice` parameter.

    We support the following categories of tools:

    - **Built-in tools**: Tools that are provided by OpenAI that extend the model's
      capabilities, like
      [web search](https://platform.openai.com/docs/guides/tools-web-search) or
      [file search](https://platform.openai.com/docs/guides/tools-file-search).
      Learn more about
      [built-in tools](https://platform.openai.com/docs/guides/tools).
    - **MCP Tools**: Integrations with third-party systems via custom MCP servers or
      predefined connectors such as Google Drive and SharePoint. Learn more about
      [MCP Tools](https://platform.openai.com/docs/guides/tools-connectors-mcp).
    - **Function calls (custom tools)**: Functions that are defined by you, enabling
      the model to call your own code with strongly typed arguments and outputs.
      Learn more about
      [function calling](https://platform.openai.com/docs/guides/function-calling).
      You can also use custom tools to call your own code.
    """

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying the number of most likely tokens to
    return at each token position, each with an associated log probability.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or `temperature` but not both.
    """

    truncation: Optional[Literal["auto", "disabled"]]
    """The truncation strategy to use for the model response.

    - `auto`: If the input to this Response exceeds the model's context window size,
      the model will truncate the response to fit the context window by dropping
      items from the beginning of the conversation.
    - `disabled` (default): If the input size will exceed the context window size
      for a model, the request will fail with a 400 error.
    """

    user: Optional[str]
    """This field is being replaced by `safety_identifier` and `prompt_cache_key`.

    Use `prompt_cache_key` instead to maintain caching optimizations. A stable
    identifier for your end-users. Used to boost cache hit rates by better bucketing
    similar requests and to help OpenAI detect and prevent abuse.
    [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).
    """


class ConversationResponseConversationParam(TypedDict, total=False):
    """Conversation reference for continuing a Responses session."""

    id: Required[str]
    """Identifier of the existing conversation."""


Conversation: TypeAlias = Union[str, ConversationResponseConversationParam]

Credentials: TypeAlias = Union[Credential, MCPCredentials]

MCPServers: TypeAlias = Union[str, MCPServerSpec, mcp_servers.MCPServers]

Model: TypeAlias = Union[str, "DedalusModel", SequenceNotStr["DedalusModelChoice"]]


class Prompt(TypedDict, total=False):
    """Stored prompt template reference (BYOK)."""

    id: Required[str]
    """Identifier of the stored prompt."""

    variables: Optional["JSONObjectInput"]
    """Variables to substitute into the stored prompt template."""

    version: Optional[str]
    """Optional version identifier of the stored prompt."""


from .shared_params.dedalus_model import DedalusModel
from .shared_params.json_object_input import JSONObjectInput
from .shared_params.dedalus_model_choice import DedalusModelChoice
