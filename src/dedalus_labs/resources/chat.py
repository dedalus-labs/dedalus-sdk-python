# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, overload

import httpx

from ..types import chat_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.completion import Completion
from ..types.stream_chunk import StreamChunk

__all__ = ["ChatResource", "AsyncChatResource"]


class ChatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return ChatResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether to stream back partial message deltas as Server-Sent Events.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          stream: Whether to stream back partial message deltas as Server-Sent Events.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion | Stream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          stream: Whether to stream back partial message deltas as Server-Sent Events.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def create(
        self,
        *,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion | Stream[StreamChunk]:
        return self._post(
            "/v1/chat",
            body=maybe_transform(
                {
                    "agent_attributes": agent_attributes,
                    "frequency_penalty": frequency_penalty,
                    "input": input,
                    "logit_bias": logit_bias,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "model": model,
                    "model_attributes": model_attributes,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "stop": stop,
                    "stream": stream,
                    "temperature": temperature,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_p": top_p,
                    "user": user,
                },
                chat_create_params.ChatCreateParamsStreaming
                if stream
                else chat_create_params.ChatCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=Stream[StreamChunk],
        )


class AsyncChatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncChatResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether to stream back partial message deltas as Server-Sent Events.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          stream: Whether to stream back partial message deltas as Server-Sent Events.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion | AsyncStream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Args:
          stream: Whether to stream back partial message deltas as Server-Sent Events.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far.

          input: Input to the model - can be messages, images, or other modalities. Supports
              OpenAI chat format with role/content structure. For multimodal inputs, content
              can include text, images, or other media types.

          logit_bias: Modify likelihood of specified tokens appearing in the completion.

          max_tokens: Maximum number of tokens to generate in the completion.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution.

          model: Model(s) to use for completion. Can be a single model ID, a Model object, or a
              list for multi-model routing.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic.

          tool_choice: Controls which tool is called by the model.

          tools: List of tools available to the model in OpenAI function calling format.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature.

          user: Unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def create(
        self,
        *,
        agent_attributes: Optional[Dict[str, float]] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        input: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_turns: Optional[int] | NotGiven = NOT_GIVEN,
        mcp_servers: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[chat_create_params.Model] | NotGiven = NOT_GIVEN,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stop: Optional[List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, object, None] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[object]] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Completion | AsyncStream[StreamChunk]:
        return await self._post(
            "/v1/chat",
            body=await async_maybe_transform(
                {
                    "agent_attributes": agent_attributes,
                    "frequency_penalty": frequency_penalty,
                    "input": input,
                    "logit_bias": logit_bias,
                    "max_tokens": max_tokens,
                    "max_turns": max_turns,
                    "mcp_servers": mcp_servers,
                    "model": model,
                    "model_attributes": model_attributes,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "stop": stop,
                    "stream": stream,
                    "temperature": temperature,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_p": top_p,
                    "user": user,
                },
                chat_create_params.ChatCreateParamsStreaming
                if stream
                else chat_create_params.ChatCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=AsyncStream[StreamChunk],
        )


class ChatResourceWithRawResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create = to_raw_response_wrapper(
            chat.create,
        )


class AsyncChatResourceWithRawResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create = async_to_raw_response_wrapper(
            chat.create,
        )


class ChatResourceWithStreamingResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create = to_streamed_response_wrapper(
            chat.create,
        )


class AsyncChatResourceWithStreamingResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create = async_to_streamed_response_wrapper(
            chat.create,
        )
