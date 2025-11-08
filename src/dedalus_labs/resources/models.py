# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..types.model import Model
from .._base_client import make_request_options
from ..types.list_models_response import ListModelsResponse

__all__ = ["ModelsResource", "AsyncModelsResource"]


class ModelsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return ModelsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Model:
        """
        Retrieve a model.

        Retrieve detailed information about a specific model, including its
        capabilities, provider, and supported features.

        Args: model_id: The ID of the model to retrieve (e.g., 'openai/gpt-4',
        'anthropic/claude-3-5-sonnet-20241022') user: Authenticated user obtained from
        API key validation

        Returns: Model: Information about the requested model

        Raises: HTTPException: - 401 if authentication fails - 404 if model not found or
        not accessible with current API key - 500 if internal error occurs

        Requires: Valid API key with 'read' scope permission

        Example: ```python import dedalus_labs

            client = dedalus_labs.Client(api_key="your-api-key")
            model = client.models.retrieve("openai/gpt-4")

            print(f"Model: {model.id}")
            print(f"Owner: {model.owned_by}")
            ```

            Response:
            ```json
            {
                "id": "openai/gpt-4",
                "object": "model",
                "created": 1687882411,
                "owned_by": "openai"
            }
            ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return self._get(
            f"/v1/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Model,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ListModelsResponse:
        """
        List available models.

        Retrieve the complete list of models available to your organization, including
        models from OpenAI, Anthropic, Google, xAI, Mistral, Fireworks, and DeepSeek.

        Returns: ListModelsResponse: List of available models across all supported
        providers
        """
        return self._get(
            "/v1/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListModelsResponse,
        )


class AsyncModelsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModelsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncModelsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModelsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncModelsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        model_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Model:
        """
        Retrieve a model.

        Retrieve detailed information about a specific model, including its
        capabilities, provider, and supported features.

        Args: model_id: The ID of the model to retrieve (e.g., 'openai/gpt-4',
        'anthropic/claude-3-5-sonnet-20241022') user: Authenticated user obtained from
        API key validation

        Returns: Model: Information about the requested model

        Raises: HTTPException: - 401 if authentication fails - 404 if model not found or
        not accessible with current API key - 500 if internal error occurs

        Requires: Valid API key with 'read' scope permission

        Example: ```python import dedalus_labs

            client = dedalus_labs.Client(api_key="your-api-key")
            model = client.models.retrieve("openai/gpt-4")

            print(f"Model: {model.id}")
            print(f"Owner: {model.owned_by}")
            ```

            Response:
            ```json
            {
                "id": "openai/gpt-4",
                "object": "model",
                "created": 1687882411,
                "owned_by": "openai"
            }
            ```

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_id:
            raise ValueError(f"Expected a non-empty value for `model_id` but received {model_id!r}")
        return await self._get(
            f"/v1/models/{model_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Model,
        )

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ListModelsResponse:
        """
        List available models.

        Retrieve the complete list of models available to your organization, including
        models from OpenAI, Anthropic, Google, xAI, Mistral, Fireworks, and DeepSeek.

        Returns: ListModelsResponse: List of available models across all supported
        providers
        """
        return await self._get(
            "/v1/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ListModelsResponse,
        )


class ModelsResourceWithRawResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.retrieve = to_raw_response_wrapper(
            models.retrieve,
        )
        self.list = to_raw_response_wrapper(
            models.list,
        )


class AsyncModelsResourceWithRawResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.retrieve = async_to_raw_response_wrapper(
            models.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            models.list,
        )


class ModelsResourceWithStreamingResponse:
    def __init__(self, models: ModelsResource) -> None:
        self._models = models

        self.retrieve = to_streamed_response_wrapper(
            models.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            models.list,
        )


class AsyncModelsResourceWithStreamingResponse:
    def __init__(self, models: AsyncModelsResource) -> None:
        self._models = models

        self.retrieve = async_to_streamed_response_wrapper(
            models.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            models.list,
        )
