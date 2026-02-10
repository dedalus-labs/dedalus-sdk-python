# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import response_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.response import Response
from ..types.shared_params.json_object_input import JSONObjectInput

__all__ = ["ResponsesResource", "AsyncResponsesResource"]


class ResponsesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return ResponsesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        background: Optional[bool] | Omit = omit,
        conversation: Optional[response_create_params.Conversation] | Omit = omit,
        credentials: Optional[response_create_params.Credentials] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        include: Optional[SequenceNotStr[str]] | Omit = omit,
        input: Union[str, Iterable[JSONObjectInput], None] | Omit = omit,
        instructions: Union[str, Iterable[JSONObjectInput], None] | Omit = omit,
        max_output_tokens: Optional[int] | Omit = omit,
        max_tool_calls: Optional[int] | Omit = omit,
        mcp_servers: Optional[response_create_params.MCPServers] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        model: Optional[response_create_params.Model] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        previous_response_id: Optional[str] | Omit = omit,
        prompt: Optional[response_create_params.Prompt] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning: Optional[JSONObjectInput] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: bool | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        text: Optional[JSONObjectInput] | Omit = omit,
        tool_choice: Union[str, JSONObjectInput, None] | Omit = omit,
        tools: Optional[Iterable[JSONObjectInput]] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        truncation: Optional[Literal["auto", "disabled"]] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Response:
        """
        Create a response using the OpenAI Responses API.

        This endpoint routes directly to OpenAI's Responses API. Only OpenAI models are
        supported.

        Args:
          background: Whether to run the model response in the background.
              [Learn more](https://platform.openai.com/docs/guides/background).

          conversation: Conversation that this response belongs to. Items from this conversation are
              prepended to the input items, and output items from this response are
              automatically added after completion.

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          frequency_penalty: Penalizes new tokens based on their frequency in the text so far.

          include: Specify additional output data to include in the model response. Currently
              supported values are:

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

          input: Text, image, or file inputs to the model, used to generate a response.

              Learn more:

              - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
              - [Image inputs](https://platform.openai.com/docs/guides/images)
              - [File inputs](https://platform.openai.com/docs/guides/pdf-files)
              - [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
              - [Function calling](https://platform.openai.com/docs/guides/function-calling)

          instructions: A system (or developer) message inserted into the model's context.

              When using along with `previous_response_id`, the instructions from a previous
              response will not be carried over to the next response. This makes it simple to
              swap out system (or developer) messages in new responses.

          max_output_tokens: An upper bound for the number of tokens that can be generated for a response,
              including visible output tokens and
              [reasoning tokens](https://platform.openai.com/docs/guides/reasoning).

          max_tool_calls: The maximum number of total calls to built-in tools that can be processed in a
              response. This maximum number applies across all built-in tool calls, not per
              individual tool. Any further attempts to call a tool by the model will be
              ignored.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          metadata: Set of up to 16 key-value string pairs that can be attached to the response for
              structured metadata and later querying via the API or dashboard.

          model: Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI offers a
              wide range of models with different capabilities, performance characteristics,
              and price points. Refer to the
              [model guide](https://platform.openai.com/docs/models) to browse and compare
              available models.

          parallel_tool_calls: Whether to allow the model to run tool calls in parallel.

          presence_penalty: Penalizes new tokens based on whether they appear in the text so far.

          previous_response_id: Unique ID of the previous response to continue from when creating multi-turn
              conversations. Cannot be used together with `conversation`.

          prompt: Stored prompt template reference (BYOK).

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          reasoning: **gpt-5 and o-series models only**

              Configuration options for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning).

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          service_tier: Specifies the processing type used for serving the request.

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

          store: Whether to store the generated response for later retrieval via the Responses
              API.

          stream: If set to true, the model response data will be streamed to the client as it is
              generated using
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format).
              See the
              [Streaming section below](https://platform.openai.com/docs/api-reference/responses-streaming)
              for more information.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. We generally recommend altering this or `top_p` but
              not both.

          text: Configuration options for a text response from the model. Can be plain text or
              structured JSON data. Learn more:

              - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
              - [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

          tool_choice: How the model should select which tool (or tools) to use when generating a
              response. See the `tools` parameter to see how to specify which tools the model
              can call.

          tools: An array of tools the model may call while generating a response. You can
              specify which tool to use by setting the `tool_choice` parameter.

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

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          truncation: The truncation strategy to use for the model response.

              - `auto`: If the input to this Response exceeds the model's context window size,
                the model will truncate the response to fit the context window by dropping
                items from the beginning of the conversation.
              - `disabled` (default): If the input size will exceed the context window size
                for a model, the request will fail with a 400 error.

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/responses",
            body=maybe_transform(
                {
                    "background": background,
                    "conversation": conversation,
                    "credentials": credentials,
                    "frequency_penalty": frequency_penalty,
                    "include": include,
                    "input": input,
                    "instructions": instructions,
                    "max_output_tokens": max_output_tokens,
                    "max_tool_calls": max_tool_calls,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "model": model,
                    "parallel_tool_calls": parallel_tool_calls,
                    "presence_penalty": presence_penalty,
                    "previous_response_id": previous_response_id,
                    "prompt": prompt,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning": reasoning,
                    "safety_identifier": safety_identifier,
                    "service_tier": service_tier,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "text": text,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "truncation": truncation,
                    "user": user,
                },
                response_create_params.ResponseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Response,
        )


class AsyncResponsesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResponsesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncResponsesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResponsesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncResponsesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        background: Optional[bool] | Omit = omit,
        conversation: Optional[response_create_params.Conversation] | Omit = omit,
        credentials: Optional[response_create_params.Credentials] | Omit = omit,
        frequency_penalty: Optional[float] | Omit = omit,
        include: Optional[SequenceNotStr[str]] | Omit = omit,
        input: Union[str, Iterable[JSONObjectInput], None] | Omit = omit,
        instructions: Union[str, Iterable[JSONObjectInput], None] | Omit = omit,
        max_output_tokens: Optional[int] | Omit = omit,
        max_tool_calls: Optional[int] | Omit = omit,
        mcp_servers: Optional[response_create_params.MCPServers] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        model: Optional[response_create_params.Model] | Omit = omit,
        parallel_tool_calls: Optional[bool] | Omit = omit,
        presence_penalty: Optional[float] | Omit = omit,
        previous_response_id: Optional[str] | Omit = omit,
        prompt: Optional[response_create_params.Prompt] | Omit = omit,
        prompt_cache_key: Optional[str] | Omit = omit,
        reasoning: Optional[JSONObjectInput] | Omit = omit,
        safety_identifier: Optional[str] | Omit = omit,
        service_tier: Optional[Literal["auto", "default"]] | Omit = omit,
        store: Optional[bool] | Omit = omit,
        stream: bool | Omit = omit,
        stream_options: Optional[JSONObjectInput] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
        text: Optional[JSONObjectInput] | Omit = omit,
        tool_choice: Union[str, JSONObjectInput, None] | Omit = omit,
        tools: Optional[Iterable[JSONObjectInput]] | Omit = omit,
        top_logprobs: Optional[int] | Omit = omit,
        top_p: Optional[float] | Omit = omit,
        truncation: Optional[Literal["auto", "disabled"]] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Response:
        """
        Create a response using the OpenAI Responses API.

        This endpoint routes directly to OpenAI's Responses API. Only OpenAI models are
        supported.

        Args:
          background: Whether to run the model response in the background.
              [Learn more](https://platform.openai.com/docs/guides/background).

          conversation: Conversation that this response belongs to. Items from this conversation are
              prepended to the input items, and output items from this response are
              automatically added after completion.

          credentials: Credentials for MCP server authentication. Each credential is matched to servers
              by connection name.

          frequency_penalty: Penalizes new tokens based on their frequency in the text so far.

          include: Specify additional output data to include in the model response. Currently
              supported values are:

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

          input: Text, image, or file inputs to the model, used to generate a response.

              Learn more:

              - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
              - [Image inputs](https://platform.openai.com/docs/guides/images)
              - [File inputs](https://platform.openai.com/docs/guides/pdf-files)
              - [Conversation state](https://platform.openai.com/docs/guides/conversation-state)
              - [Function calling](https://platform.openai.com/docs/guides/function-calling)

          instructions: A system (or developer) message inserted into the model's context.

              When using along with `previous_response_id`, the instructions from a previous
              response will not be carried over to the next response. This makes it simple to
              swap out system (or developer) messages in new responses.

          max_output_tokens: An upper bound for the number of tokens that can be generated for a response,
              including visible output tokens and
              [reasoning tokens](https://platform.openai.com/docs/guides/reasoning).

          max_tool_calls: The maximum number of total calls to built-in tools that can be processed in a
              response. This maximum number applies across all built-in tool calls, not per
              individual tool. Any further attempts to call a tool by the model will be
              ignored.

          mcp_servers: MCP server identifiers. Accepts marketplace slugs, URLs, or MCPServerSpec
              objects. MCP tools are executed server-side and billed separately.

          metadata: Set of up to 16 key-value string pairs that can be attached to the response for
              structured metadata and later querying via the API or dashboard.

          model: Model ID used to generate the response, like `gpt-4o` or `o3`. OpenAI offers a
              wide range of models with different capabilities, performance characteristics,
              and price points. Refer to the
              [model guide](https://platform.openai.com/docs/models) to browse and compare
              available models.

          parallel_tool_calls: Whether to allow the model to run tool calls in parallel.

          presence_penalty: Penalizes new tokens based on whether they appear in the text so far.

          previous_response_id: Unique ID of the previous response to continue from when creating multi-turn
              conversations. Cannot be used together with `conversation`.

          prompt: Stored prompt template reference (BYOK).

          prompt_cache_key: Used by OpenAI to cache responses for similar requests to optimize your cache
              hit rates. Replaces the `user` field.
              [Learn more](https://platform.openai.com/docs/guides/prompt-caching).

          reasoning: **gpt-5 and o-series models only**

              Configuration options for
              [reasoning models](https://platform.openai.com/docs/guides/reasoning).

          safety_identifier: A stable identifier used to help detect users of your application that may be
              violating OpenAI's usage policies. The IDs should be a string that uniquely
              identifies each user. We recommend hashing their username or email address, in
              order to avoid sending us any identifying information.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          service_tier: Specifies the processing type used for serving the request.

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

          store: Whether to store the generated response for later retrieval via the Responses
              API.

          stream: If set to true, the model response data will be streamed to the client as it is
              generated using
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format).
              See the
              [Streaming section below](https://platform.openai.com/docs/api-reference/responses-streaming)
              for more information.

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. We generally recommend altering this or `top_p` but
              not both.

          text: Configuration options for a text response from the model. Can be plain text or
              structured JSON data. Learn more:

              - [Text inputs and outputs](https://platform.openai.com/docs/guides/text)
              - [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)

          tool_choice: How the model should select which tool (or tools) to use when generating a
              response. See the `tools` parameter to see how to specify which tools the model
              can call.

          tools: An array of tools the model may call while generating a response. You can
              specify which tool to use by setting the `tool_choice` parameter.

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

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          truncation: The truncation strategy to use for the model response.

              - `auto`: If the input to this Response exceeds the model's context window size,
                the model will truncate the response to fit the context window by dropping
                items from the beginning of the conversation.
              - `disabled` (default): If the input size will exceed the context window size
                for a model, the request will fail with a 400 error.

          user: This field is being replaced by `safety_identifier` and `prompt_cache_key`. Use
              `prompt_cache_key` instead to maintain caching optimizations. A stable
              identifier for your end-users. Used to boost cache hit rates by better bucketing
              similar requests and to help OpenAI detect and prevent abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#safety-identifiers).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/responses",
            body=await async_maybe_transform(
                {
                    "background": background,
                    "conversation": conversation,
                    "credentials": credentials,
                    "frequency_penalty": frequency_penalty,
                    "include": include,
                    "input": input,
                    "instructions": instructions,
                    "max_output_tokens": max_output_tokens,
                    "max_tool_calls": max_tool_calls,
                    "mcp_servers": mcp_servers,
                    "metadata": metadata,
                    "model": model,
                    "parallel_tool_calls": parallel_tool_calls,
                    "presence_penalty": presence_penalty,
                    "previous_response_id": previous_response_id,
                    "prompt": prompt,
                    "prompt_cache_key": prompt_cache_key,
                    "reasoning": reasoning,
                    "safety_identifier": safety_identifier,
                    "service_tier": service_tier,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "text": text,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "truncation": truncation,
                    "user": user,
                },
                response_create_params.ResponseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=Response,
        )


class ResponsesResourceWithRawResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.create = to_raw_response_wrapper(
            responses.create,
        )


class AsyncResponsesResourceWithRawResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.create = async_to_raw_response_wrapper(
            responses.create,
        )


class ResponsesResourceWithStreamingResponse:
    def __init__(self, responses: ResponsesResource) -> None:
        self._responses = responses

        self.create = to_streamed_response_wrapper(
            responses.create,
        )


class AsyncResponsesResourceWithStreamingResponse:
    def __init__(self, responses: AsyncResponsesResource) -> None:
        self._responses = responses

        self.create = async_to_streamed_response_wrapper(
            responses.create,
        )
