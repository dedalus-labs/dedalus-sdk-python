# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import partial
from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, overload

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._streaming import Stream, AsyncStream
from ...types.chat import ChatCompletionAudioParam, completion_create_params
from ..._base_client import make_request_options
from ...types.chat.chat_completion import ChatCompletion
from ...types.chat.chat_completion_chunk import ChatCompletionChunk
from ...lib._parsing import (
    ResponseFormatT,
    parse_chat_completion as _parse_chat_completion,
    type_to_response_format_param as _type_to_response_format,
    validate_input_tools as _validate_input_tools,
)
from ...lib.streaming.chat import (
    ChatCompletionStreamManager,
    AsyncChatCompletionStreamManager,
)
from ...types.chat.prediction_content_param import PredictionContentParam
from ...types.shared_params.json_object_input import JSONObjectInput
from ...types.chat.chat_completion_audio_param import ChatCompletionAudioParam
from ...types.chat.chat_completion_functions_param import ChatCompletionFunctionsParam

__all__ = ["CompletionsResource", "AsyncCompletionsResource"]


class CompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return CompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        model: completion_create_params.Model,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream: Enable streaming response

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def create(
        self,
        *,
        model: completion_create_params.Model,
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[ChatCompletionChunk]:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          stream: Enable streaming response

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    def create(
        self,
        *,
        model: completion_create_params.Model,
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          stream: Enable streaming response

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model"], ["model", "stream"])
    def create(
        self,
        *,
        model: completion_create_params.Model,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Literal[True] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        import inspect
        import pydantic
        from ..._utils import is_given

        # Validate response_format is not a Pydantic model
        if (
            is_given(response_format)
            and inspect.isclass(response_format)
            and issubclass(response_format, pydantic.BaseModel)
        ):
            raise TypeError(
                "You tried to pass a `BaseModel` class to `chat.completions.create()`; "
                "You must use `chat.completions.parse()` instead"
            )

        return self._post(
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "cached_content": cached_content,
                    "credentials": credentials,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "messages": messages,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "prompt_cache_retention": prompt_cache_retention,
                    "prompt_mode": prompt_mode,
                    "reasoning_effort": reasoning_effort,
                    "response_format": response_format,
                    "safe_prompt": safe_prompt,
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "system_instruction": system_instruction,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ChatCompletion,
            stream=stream or False,
            stream_cls=Stream[ChatCompletionChunk],
        )

    def parse(
        self,
        *,
        model: completion_create_params.Model,
        response_format: type[ResponseFormatT] | Omit = omit,
        messages: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        input: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        instructions: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Union[str, Dict[str, object], None] | Omit = omit,
        functions: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Union[str, SequenceNotStr[str], None] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[Dict[str, object]] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning_effort: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ):
        """Parse method with Pydantic model support for structured outputs.

        Accepts a Pydantic BaseModel class via response_format parameter and returns
        a ParsedChatCompletion with automatic JSON parsing into the model.

        Example:
            from pydantic import BaseModel

            class PersonInfo(BaseModel):
                name: str
                age: int

            completion = client.chat.completions.parse(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Tell me about Alice, age 28"}],
                response_format=PersonInfo,
            )

            person = completion.choices[0].message.parsed
        """
        from ...types.chat.parsed_chat_completion import ParsedChatCompletion
        from ..._utils import is_given

        chat_completion_tools = _validate_input_tools(tools)

        extra_headers = {
            "X-Stainless-Helper-Method": "chat.completions.parse",
            **(extra_headers or {}),
        }

        def parser(raw_completion: Completion):
            return _parse_chat_completion(
                response_format=response_format,
                chat_completion=raw_completion,
                input_tools=chat_completion_tools,
            )

        return self._post(
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "input": input,
                    "instructions": instructions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning_effort": reasoning_effort,
                    "response_format": _type_to_response_format(response_format),
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": False,
                    "stream_options": stream_options,
                    "system": system,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                post_parser=parser,
            ),
            cast_to=ParsedChatCompletion,
        )

    def stream(
        self,
        *,
        model: completion_create_params.Model,
        messages: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        response_format: type[ResponseFormatT] | Omit = omit,
        input: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        instructions: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        system: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Union[str, Dict[str, object], None] | Omit = omit,
        functions: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Union[str, SequenceNotStr[str], None] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[Dict[str, object]] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning_effort: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletionStreamManager[ResponseFormatT]:
        """Stream chat completions with the same structured parsing guarantees as `.parse()`."""

        chat_completion_tools = _validate_input_tools(tools)
        extra_headers = {
            "X-Stainless-Helper-Method": "chat.completions.stream",
            **(extra_headers or {}),
        }

        api_request = partial(
            self._post,
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "input": input,
                    "instructions": instructions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning_effort": reasoning_effort,
                    "response_format": _type_to_response_format(response_format),
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": True,
                    "stream_options": stream_options,
                    "system": system,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParamsStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ChatCompletion,
            stream=True,
            stream_cls=Stream[ChatCompletionChunk],
        )

        return ChatCompletionStreamManager(
            api_request,
            response_format=response_format,
            input_tools=chat_completion_tools,
        )


class AsyncCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        model: completion_create_params.Model,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream: Enable streaming response

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def create(
        self,
        *,
        model: completion_create_params.Model,
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[ChatCompletionChunk]:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          stream: Enable streaming response

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @overload
    async def create(
        self,
        *,
        model: completion_create_params.Model,
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        """
        Create a chat completion.

        Generates a model response for the given conversation and configuration.
        Supports OpenAI-compatible parameters and provider-specific extensions.

        Headers:

        - Authorization: bearer key for the calling account.
        - Optional BYOK or provider headers if applicable.

        Behavior:

        - If multiple models are supplied, the first one is used, and the agent may hand
          off to another model.
        - Tools may be invoked on the server or signaled for the client to run.
        - Streaming responses emit incremental deltas; non-streaming returns a single
          object.
        - Usage metrics are computed when available and returned in the response.

        Responses:

        - 200 OK: JSON completion object with choices, message content, and usage.
        - 400 Bad Request: validation error.
        - 401 Unauthorized: authentication failed.
        - 402 Payment Required or 429 Too Many Requests: quota, balance, or rate limit
          issue.
        - 500 Internal Server Error: unexpected failure.

        Billing:

        - Token usage metered by the selected model(s).
        - Tool calls and MCP sessions may be billed separately.
        - Streaming is settled after the stream ends via an async task.

        Example (non-streaming HTTP): POST /v1/chat/completions Content-Type:
        application/json Authorization: Bearer <key>

        { "model": "provider/model-name", "messages": [{"role": "user", "content":
        "Hello"}] }

        200 OK { "id": "cmpl_123", "object": "chat.completion", "choices": [ {"index":
        0, "message": {"role": "assistant", "content": "Hi there!"}, "finish_reason":
        "stop"} ], "usage": {"prompt_tokens": 3, "completion_tokens": 4, "total_tokens":
        7} }

        Example (streaming over SSE): POST /v1/chat/completions Accept:
        text/event-stream

        data: {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":"Hi"}}]} data:
        {"id":"cmpl_123","choices":[{"index":0,"delta":{"content":" there!"}}]} data:
        [DONE]

        Args:
          model: Model identifier. Accepts model ID strings, lists for routing, or DedalusModel
              objects with per-model settings.

          stream: Enable streaming response

          agent_attributes: Agent attributes. Values in [0.0, 1.0].

          audio: Parameters for audio output. Required when audio output is requested with
              `modalities: ["audio"]`.
              [Learn more](https://platform.openai.com/docs/guides/audio).

              Fields:

              - voice (required): VoiceIdsShared
              - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content
              [cached](https://ai.google.dev/gemini-api/docs/caching) to use as context to
              serve the prediction. Format: `cachedContents/{cachedContent}`

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the
              deferred response by GET `/v1/chat/deferred-completion/{request_id}`.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate JSON
              inputs for.

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accepts a
              JSON object that maps tokens (specified by their token ID in the tokenizer) to
              an associated bias value from -100 to 100. Mathematically, the bias is added to
              the logits generated by the model prior to sampling. The exact effect will vary
              per model, but values between -1 and 1 should decrease or increase likelihood of
              selection; values like -100 or 100 should result in a ban or exclusive selection
              of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be useful
              for storing additional information about the object in a structured format, and
              querying for objects via API or the dashboard. Keys are strings with a maximum
              length of 64 characters. Values are strings with a maximum length of 512
              characters.

          modalities: Output types that you would like the model to generate. Most models are capable
              of generating text, which is the default: `["text"]` The `gpt-4o-audio-preview`
              model can also be used to
              [generate audio](https://platform.openai.com/docs/guides/audio). To request that
              this model generate both text and audio responses, you can use:
              `["text", "audio"]`

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note that
              you will be charged based on the number of generated tokens across all of the
              choices. Keep `n` as `1` to minimize costs.

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended
              prompt caching, which keeps cached prefixes active for longer, up to a maximum
              of 24 hours.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to
              `reasoning` the system prompt for reasoning models will be used.

          reasoning_effort: Constrains effort on reasoning for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning). Currently
              supported values are `none`, `minimal`, `low`, `medium`, and `high`. Reducing
              reasoning effort can result in faster responses and fewer tokens used on
              reasoning in a response. - `gpt-5.1` defaults to `none`, which does not perform
              reasoning. The supported reasoning values for `gpt-5.1` are `none`, `low`,
              `medium`, and `high`. Tool calls are supported for all reasoning values in
              gpt-5.1. - All models before `gpt-5.1` default to `medium` reasoning effort, and
              do not support `none`. - The `gpt-5-pro` model defaults to (and only supports)
              `high` reasoning effort.

          response_format: An object specifying the format that the model must output. Setting to
              `{ "type": "json_schema", "json_schema": {...} }` enables Structured Outputs
              which ensures the model will match your supplied JSON schema. Learn more in the
              [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
              Setting to `{ "type": "json_object" }` enables the older JSON mode, which
              ensures the message the model generates is valid JSON. Using `json_schema` is
              preferred for models that support it.

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be
              acquired by the model.

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in
              our [model distillation](https://platform.openai.com/docs/guides/distillation)
              or [evals](https://platform.openai.com/docs/guides/evals) products. Supports
              text and image inputs. Note: image inputs over 8MB will be dropped.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
              not call any tool and instead generates a message. `auto` means the model can
              pick between generating a message or calling one or more tools. `required` means
              the model must call one or more tools. Specifying a particular tool via
              `{"type": "function", "function": {"name": "my_function"}}` forces the model to
              call that tool. `none` is the default when no tools are present. `auto` is the
              default if tools are present.

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          verbosity: Constrains the verbosity of the model's response. Lower values will result in
              more concise responses, while higher values will result in more verbose
              responses. Currently supported values are `low`, `medium`, and `high`.

          web_search_options: This tool searches the web for relevant results to use in a response. Learn more
              about the
              [web search tool](https://platform.openai.com/docs/guides/tools-web-search?api-mode=chat).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["model"], ["model", "stream"])
    async def create(
        self,
        *,
        model: completion_create_params.Model,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[ChatCompletionAudioParam] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[JSONObjectInput] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[JSONObjectInput] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[PredictionContentParam] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        prompt_cache_retention: Optional[str] | Omit = omit,
        prompt_mode: Optional[Literal["reasoning"]] | Omit = omit,
        reasoning_effort: Optional[str] | Omit = omit,
        response_format: Optional[completion_create_params.ResponseFormat] | Omit = omit,
        safe_prompt: Optional[bool] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[completion_create_params.SafetySetting]] | Omit = omit,
        search_parameters: Optional[JSONObjectInput] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Literal[True] | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        system_instruction: Union[JSONObjectInput, str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[JSONObjectInput] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[JSONObjectInput] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        import inspect
        import pydantic
        from ..._utils import is_given

        # Validate response_format is not a Pydantic model
        if (
            is_given(response_format)
            and inspect.isclass(response_format)
            and issubclass(response_format, pydantic.BaseModel)
        ):
            raise TypeError(
                "You tried to pass a `BaseModel` class to `chat.completions.create()`; "
                "You must use `chat.completions.parse()` instead"
            )

        return await self._post(
            "/v1/chat/completions",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "cached_content": cached_content,
                    "credentials": credentials,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "messages": messages,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "prompt_cache_retention": prompt_cache_retention,
                    "prompt_mode": prompt_mode,
                    "reasoning_effort": reasoning_effort,
                    "response_format": response_format,
                    "safe_prompt": safe_prompt,
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "system_instruction": system_instruction,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ChatCompletion,
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionChunk],
        )

    async def parse(
        self,
        *,
        model: completion_create_params.Model,
        response_format: type[ResponseFormatT] | Omit = omit,
        messages: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        input: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        instructions: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Union[str, Dict[str, object], None] | Omit = omit,
        functions: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Union[str, SequenceNotStr[str], None] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[Dict[str, object]] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning_effort: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ):
        """Async parse method with Pydantic model support for structured outputs."""
        from ...types.chat.parsed_chat_completion import ParsedChatCompletion
        from ..._utils import is_given

        chat_completion_tools = _validate_input_tools(tools)

        extra_headers = {
            "X-Stainless-Helper-Method": "chat.completions.parse",
            **(extra_headers or {}),
        }

        def parser(raw_completion: Completion):
            return _parse_chat_completion(
                response_format=response_format,
                chat_completion=raw_completion,
                input_tools=chat_completion_tools,
            )

        return await self._post(
            "/v1/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "input": input,
                    "instructions": instructions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning_effort": reasoning_effort,
                    "response_format": _type_to_response_format(response_format),
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": False,
                    "stream_options": stream_options,
                    "system": system,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
                post_parser=parser,
            ),
            cast_to=ParsedChatCompletion,
        )

    def stream(
        self,
        *,
        model: completion_create_params.Model,
        messages: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        response_format: type[ResponseFormatT] | Omit = omit,
        input: Union[Iterable[Dict[str, object]], str, None] | Omit = omit,
        instructions: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        system: Union[str, Iterable[Dict[str, object]], None] | Omit = omit,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Union[str, Dict[str, object], None] | Omit = omit,
        functions: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Union[str, SequenceNotStr[str], None] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        prediction: Optional[Dict[str, object]] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning_effort: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        safety_settings: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[Literal["low", "medium", "high"]] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncChatCompletionStreamManager[ResponseFormatT]:
        """Async variant of `stream()` with identical semantics."""

        chat_completion_tools = _validate_input_tools(tools)
        extra_headers = {
            "X-Stainless-Helper-Method": "chat.completions.stream",
            **(extra_headers or {}),
        }

        api_request = self._post(
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "agent_attributes": agent_attributes,
                    "audio": audio,
                    "automatic_tool_execution": automatic_tool_execution,
                    "deferred": deferred,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "generation_config": generation_config,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
                    "input": input,
                    "instructions": instructions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "modalities": modalities,
                    "model_attributes": model_attributes,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning_effort": reasoning_effort,
                    "response_format": _type_to_response_format(response_format),
                    "safety_identifier": safety_identifier,
                    "safety_settings": safety_settings,
                    "search_parameters": search_parameters,
                    "seed": seed,
                    "service_tier": service_tier,
                    "stop": stop,
                    "store": store,
                    "stream": True,
                    "stream_options": stream_options,
                    "system": system,
                    "temperature": temperature,
                    "thinking": thinking,
                    "tool_choice": tool_choice,
                    "tool_config": tool_config,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "user": user,
                    "verbosity": verbosity,
                    "web_search_options": web_search_options,
                },
                completion_create_params.CompletionCreateParamsStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ChatCompletion,
            stream=True,
            stream_cls=AsyncStream[ChatCompletionChunk],
        )

        return AsyncChatCompletionStreamManager(
            api_request,
            response_format=response_format,
            input_tools=chat_completion_tools,
        )


class CompletionsResourceWithRawResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithRawResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_raw_response_wrapper(
            completions.create,
        )


class CompletionsResourceWithStreamingResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithStreamingResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
