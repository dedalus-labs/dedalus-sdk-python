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
from ...types.chat.stream_chunk import StreamChunk

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
        messages: Iterable[Dict[str, object]],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

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
        messages: Iterable[Dict[str, object]],
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Stream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

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
        messages: Iterable[Dict[str, object]],
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk | Stream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["messages"], ["messages", "stream"])
    def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk | Stream[StreamChunk]:
        return self._post(
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "agent_attributes": agent_attributes,
                    "frequency_penalty": frequency_penalty,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
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
            cast_to=StreamChunk,
            stream=stream or False,
            stream_cls=Stream[StreamChunk],
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
        messages: Iterable[Dict[str, object]],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

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
        messages: Iterable[Dict[str, object]],
        stream: Literal[True],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> AsyncStream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

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
        messages: Iterable[Dict[str, object]],
        stream: bool,
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk | AsyncStream[StreamChunk]:
        """
        Create a chat completion using the Agent framework.

        This endpoint provides a vendor-agnostic chat completion API that works with
        100+ LLM providers via the Agent framework. It supports both single and
        multi-model routing, client-side and server-side tool execution, and integration
        with MCP (Model Context Protocol) servers.

        Features: - Cross-vendor compatibility (OpenAI, Anthropic, Cohere, etc.) -
        Multi-model routing with intelligent agentic handoffs - Client-side tool
        execution (tools returned as JSON) - Server-side MCP tool execution with
        automatic billing - Streaming and non-streaming responses - Advanced agent
        attributes for routing decisions - Automatic usage tracking and billing

        Args: request: Chat completion request with messages, model, and configuration
        http_request: FastAPI request object for accessing headers and state
        background_tasks: FastAPI background tasks for async billing operations user:
        Authenticated user with validated API key and sufficient balance

        Returns: ChatCompletion: OpenAI-compatible completion response with usage data

        Raises: HTTPException: - 401 if authentication fails or insufficient balance -
        400 if request validation fails - 500 if internal processing error occurs

        Billing: - Token usage billed automatically based on model pricing - MCP tool
        calls billed separately using credits system - Streaming responses billed after
        completion via background task

        Example: Basic chat completion: ```python from dedalus_labs import Dedalus

            client = Dedalus(api_key="your-api-key")

            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
            )

            print(completion.choices[0].message.content)
            ```

            With tools and MCP servers:
            ```python
            completion = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Search for recent AI news"}],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "search_web",
                            "description": "Search the web for information",
                        },
                    }
                ],
                mcp_servers=["dedalus-labs/brave-search"],
            )
            ```

            Multi-model routing:
            ```python
            completion = client.chat.completions.create(
                model=[
                    "openai/gpt-4o-mini",
                    "openai/gpt-5",
                    "anthropic/claude-sonnet-4-20250514",
                ],
                messages=[{"role": "user", "content": "Analyze this complex data"}],
                agent_attributes={"complexity": 0.8, "accuracy": 0.9},
            )
            ```

            Streaming response:
            ```python
            stream = client.chat.completions.create(
                model="openai/gpt-5",
                messages=[{"role": "user", "content": "Tell me a story"}],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end="")
            ```

        Args:
          messages: Messages to the model. Supports role/content structure and multimodal content
              arrays.

          stream: Whether to stream back partial message deltas as Server-Sent Events. When true,
              partial message deltas will be sent as OpenAI-compatible chunks.

          agent_attributes: Attributes for the agent itself, influencing behavior and model selection.
              Format: {'attribute': value}, where values are 0.0-1.0. Common attributes:
              'complexity', 'accuracy', 'efficiency', 'creativity', 'friendliness'. Higher
              values indicate stronger preference for that characteristic.

          frequency_penalty: Frequency penalty (-2 to 2). Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing likelihood of repeated
              phrases.

          guardrails: Guardrails to apply to the agent for input/output validation and safety checks.
              Reserved for future use - guardrails configuration format not yet finalized.

          handoff_config: Configuration for multi-model handoffs and agent orchestration. Reserved for
              future use - handoff configuration format not yet finalized.

          logit_bias: Modify likelihood of specified tokens appearing in the completion. Maps token
              IDs (as strings) to bias values (-100 to 100). -100 = completely ban token, +100
              = strongly favor token.

          max_tokens: Maximum number of tokens to generate in the completion. Does not include tokens
              in the input messages.

          max_turns: Maximum number of turns for agent execution before terminating (default: 10).
              Each turn represents one model inference cycle. Higher values allow more complex
              reasoning but increase cost and latency.

          mcp_servers: MCP (Model Context Protocol) server addresses to make available for server-side
              tool execution. Can be URLs (e.g., 'https://mcp.example.com') or slugs (e.g.,
              'dedalus-labs/brave-search'). MCP tools are executed server-side and billed
              separately.

          model: Model(s) to use for completion. Can be a single model ID, a DedalusModel object,
              or a list for multi-model routing. Single model: 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o-mini', or a DedalusModel
              instance. Multi-model routing: ['openai/gpt-4o-mini', 'openai/gpt-4',
              'anthropic/claude-3-5-sonnet'] or list of DedalusModel objects - agent will
              choose optimal model based on task complexity.

          model_attributes: Attributes for individual models used in routing decisions during multi-model
              execution. Format: {'model_name': {'attribute': value}}, where values are
              0.0-1.0. Common attributes: 'intelligence', 'speed', 'cost', 'creativity',
              'accuracy'. Used by agent to select optimal model based on task requirements.

          n: Number of completions to generate. Note: only n=1 is currently supported.

          presence_penalty: Presence penalty (-2 to 2). Positive values penalize new tokens based on whether
              they appear in the text so far, encouraging the model to talk about new topics.

          stop: Up to 4 sequences where the API will stop generating further tokens. The model
              will stop as soon as it encounters any of these sequences.

          temperature: Sampling temperature (0 to 2). Higher values make output more random, lower
              values make it more focused and deterministic. 0 = deterministic, 1 = balanced,
              2 = very creative.

          tool_choice: Controls which tool is called by the model. Options: 'auto' (default), 'none',
              'required', or specific tool name. Can also be a dict specifying a particular
              tool.

          tools: list of tools available to the model in OpenAI function calling format. Tools
              are executed client-side and returned as JSON for the application to handle. Use
              'mcp_servers' for server-side tool execution.

          top_p: Nucleus sampling parameter (0 to 1). Alternative to temperature. 0.1 = only top
              10% probability mass, 1.0 = consider all tokens.

          user: Unique identifier representing your end-user. Used for monitoring and abuse
              detection. Should be consistent across requests from the same user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        ...

    @required_args(["messages"], ["messages", "stream"])
    async def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        agent_attributes: Optional[Dict[str, float]] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        guardrails: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        handoff_config: Optional[Dict[str, object]] | Omit = omit,
        logit_bias: Optional[Dict[str, int]] | Omit = omit,
        max_tokens: Optional[int] | Omit = omit,
        max_turns: Optional[int] | Omit = omit,
        mcp_servers: Optional[SequenceNotStr[str]] | Omit = omit,
        model: Optional[completion_create_params.Model] | Omit = omit,
        model_attributes: Optional[Dict[str, Dict[str, float]]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        stop: Optional[SequenceNotStr[str]] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        tool_choice: Union[str, Dict[str, object], None] | Omit = omit,
        tools: Optional[Iterable[Dict[str, object]]] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> StreamChunk | AsyncStream[StreamChunk]:
        return await self._post(
            "/v1/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "agent_attributes": agent_attributes,
                    "frequency_penalty": frequency_penalty,
                    "guardrails": guardrails,
                    "handoff_config": handoff_config,
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
            cast_to=StreamChunk,
            stream=stream or False,
            stream_cls=AsyncStream[StreamChunk],
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
