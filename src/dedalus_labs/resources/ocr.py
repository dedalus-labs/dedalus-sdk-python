# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import ocr_process_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.ocr_response import OcrResponse
from ..types.ocr_document_param import OcrDocumentParam

__all__ = ["OcrResource", "AsyncOcrResource"]


class OcrResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OcrResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OcrResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OcrResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return OcrResourceWithStreamingResponse(self)

    def process(
        self,
        *,
        document: OcrDocumentParam,
        model: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> OcrResponse:
        """
        Process a document through Mistral OCR.

        Extracts text from PDFs and images, returning markdown-formatted content.

        Args:
          document: Document input for OCR.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/ocr",
            body=maybe_transform(
                {
                    "document": document,
                    "model": model,
                },
                ocr_process_params.OcrProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OcrResponse,
        )


class AsyncOcrResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOcrResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOcrResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOcrResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncOcrResourceWithStreamingResponse(self)

    async def process(
        self,
        *,
        document: OcrDocumentParam,
        model: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> OcrResponse:
        """
        Process a document through Mistral OCR.

        Extracts text from PDFs and images, returning markdown-formatted content.

        Args:
          document: Document input for OCR.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/ocr",
            body=await async_maybe_transform(
                {
                    "document": document,
                    "model": model,
                },
                ocr_process_params.OcrProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=OcrResponse,
        )


class OcrResourceWithRawResponse:
    def __init__(self, ocr: OcrResource) -> None:
        self._ocr = ocr

        self.process = to_raw_response_wrapper(
            ocr.process,
        )


class AsyncOcrResourceWithRawResponse:
    def __init__(self, ocr: AsyncOcrResource) -> None:
        self._ocr = ocr

        self.process = async_to_raw_response_wrapper(
            ocr.process,
        )


class OcrResourceWithStreamingResponse:
    def __init__(self, ocr: OcrResource) -> None:
        self._ocr = ocr

        self.process = to_streamed_response_wrapper(
            ocr.process,
        )


class AsyncOcrResourceWithStreamingResponse:
    def __init__(self, ocr: AsyncOcrResource) -> None:
        self._ocr = ocr

        self.process = async_to_streamed_response_wrapper(
            ocr.process,
        )
