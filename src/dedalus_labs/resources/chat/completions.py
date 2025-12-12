# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ...types.chat import completion_create_params
from ..._base_client import make_request_options
from ...types.chat.chat_completion import ChatCompletion
from ...types.chat.chat_completion_chunk import ChatCompletionChunk
from ...types.chat.prediction_content_param import PredictionContentParam
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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream: Enable streaming response

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Literal[True] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream: Enable streaming response

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
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

          audio: Parameters for audio output. Required when audio output is requested with `mo...

          automatic_tool_execution: Execute tools server-side. If false, returns raw tool calls for manual handling.

          cached_content: Optional. The name of the content [cached](https://ai.google.dev/gemini-api/d...

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          deferred: If set to `true`, the request returns a `request_id`. You can then get the de...

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on the...

          function_call: Wrapper for union variant: function call mode.

          functions: Deprecated in favor of `tools`. A list of functions the model may generate J...

          generation_config: Generation parameters wrapper (Google-specific)

          guardrails: Content filtering and safety policy configuration.

          handoff_config: Configuration for multi-model handoffs.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Accep...

          logprobs: Whether to return log probabilities of the output tokens or not. If true, ret...

          max_completion_tokens: Maximum tokens in completion (newer parameter name)

          max_tokens: Maximum tokens in completion

          max_turns: Maximum conversation turns.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          messages: Conversation history (OpenAI: messages, Google: contents, Responses: input)

          metadata: Set of 16 key-value pairs that can be attached to an object. This can be usef...

          modalities: Output types that you would like the model to generate. Most models are capab...

          model_attributes: Model attributes for routing. Maps model IDs to attribute dictionaries with
              values in [0.0, 1.0].

          n: How many chat completion choices to generate for each input message. Note tha...

          parallel_tool_calls: Whether to enable parallel tool calls (Anthropic uses inverted polarity)

          prediction: Static predicted output content, such as the content of a text file that is
              being regenerated.

              Fields:

              - type (required): Literal["content"]
              - content (required): str |
                Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1),
                ArrayTitle("PredictionContentArray")]

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whe...

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache...

          prompt_cache_retention: The retention policy for the prompt cache. Set to `24h` to enable extended pr...

          prompt_mode: Allows toggling between the reasoning mode and no system prompt. When set to ...

          reasoning_effort: Constrains effort on reasoning for [reasoning models](https://platform.openai...

          response_format: An object specifying the format that the model must output. Setting to `{ "...

          safe_prompt: Whether to inject a safety prompt before all conversations.

          safety_identifier: A stable identifier used to help detect users of your application that may be...

          safety_settings: Safety/content filtering settings (Google-specific)

          search_parameters: Set the parameters to be used for searched data. If not set, no data will be ...

          seed: Random seed for deterministic output

          service_tier: Service tier for request processing

          stop: Sequences that stop generation

          store: Whether or not to store the output of this chat completion request for use in...

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          system_instruction: System instruction/prompt

          temperature: Sampling temperature (0-2 for most providers)

          thinking: Extended thinking configuration (Anthropic-specific)

          tool_choice: Controls which (if any) tool is called by the model. `none` means the model w...

          tool_config: Tool calling configuration (Google-specific)

          tools: Available tools/functions for the model

          top_k: Top-k sampling parameter

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to re...

          top_p: Nucleus sampling threshold

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. U...

          verbosity: Constrains the verbosity of the model's response. Lower values will result in...

          web_search_options: This tool searches the web for relevant results to use in a response. Learn m...

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
        audio: Optional[Dict[str, object]] | Omit = omit,
        automatic_tool_execution: bool | Omit = omit,
        cached_content: Optional[str] | Omit = omit,
        credentials: Optional[completion_create_params.Credentials] | Omit = omit,
        deferred: Optional[bool] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        function_call: Optional[str] | Omit = omit,
        functions: Optional[Iterable[ChatCompletionFunctionsParam]] | Omit = omit,
        generation_config: Optional[Dict[str, object]] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        logprobs: Optional[bool] | Omit = omit,
        max_completion_tokens: Optional[int] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[completion_create_params.MCPServers] | Omit = omit,
        messages: Optional[Iterable[completion_create_params.Message]] | Omit = omit,
        metadata: Optional[Dict[str, object]] | Omit = omit,
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
        search_parameters: Optional[Dict[str, object]] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        service_tier: Optional[str] | Omit = omit,
        stop: Union[SequenceNotStr[str], str, None] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: Optional[Literal[False]] | Literal[True] | Omit = omit,
        stream_options: Optional[Dict[str, object]] | Omit = omit,
        system_instruction: Union[Dict[str, object], str, None] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        thinking: Optional[completion_create_params.Thinking] | Omit = omit,
        tool_choice: Optional[completion_create_params.ToolChoice] | Omit = omit,
        tool_config: Optional[Dict[str, object]] | Omit = omit,
        tools: Optional[Iterable[completion_create_params.Tool]] | Omit = omit,
        top_k: Optional[int] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        verbosity: Optional[str] | Omit = omit,
        web_search_options: Optional[Dict[str, object]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
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
