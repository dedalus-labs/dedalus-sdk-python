# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, Optional, cast
from typing_extensions import Literal

import httpx

from ..types import image_edit_params, image_generate_params, image_create_variation_params
from .._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.images_response import ImagesResponse

__all__ = ["ImagesResource", "AsyncImagesResource"]


class ImagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return ImagesResourceWithStreamingResponse(self)

    def create_variation(
        self,
        *,
        image: FileTypes,
        model: Optional[str] | Omit = omit,
        n: Optional[int] | Omit = omit,
        response_format: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """Create variations of an image.

        DALL·E 2 only.

        Upload an image to generate variations.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v1/images/variations",
            body=maybe_transform(body, image_create_variation_params.ImageCreateVariationParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )

    def edit(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: Optional[FileTypes] | Omit = omit,
        model: Optional[str] | Omit = omit,
        n: Optional[int] | Omit = omit,
        response_format: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """Edit images using inpainting.

        Supports dall-e-2 and gpt-image-1.

        Upload an image and optionally a mask to
        indicate which areas to regenerate based on the prompt.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v1/images/edits",
            body=maybe_transform(body, image_edit_params.ImageEditParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )

    def generate(
        self,
        *,
        prompt: str,
        background: Optional[Literal["transparent", "opaque", "auto"]] | Omit = omit,
        model: Optional[str] | Omit = omit,
        moderation: Optional[Literal["low", "auto"]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        output_compression: Optional[int] | Omit = omit,
        output_format: Optional[Literal["png", "jpeg", "webp"]] | Omit = omit,
        partial_images: Optional[int] | Omit = omit,
        quality: Optional[Literal["auto", "high", "medium", "low", "hd", "standard"]] | Omit = omit,
        response_format: Optional[Literal["url", "b64_json"]] | Omit = omit,
        size: Optional[
            Literal["256x256", "512x512", "1024x1024", "1536x1024", "1024x1536", "1792x1024", "1024x1792", "auto"]
        ]
        | Omit = omit,
        stream: Optional[bool] | Omit = omit,
        style: Optional[Literal["vivid", "natural"]] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """
        Generate images from text prompts.

        Pure image generation models only (DALL-E, GPT Image). For multimodal models
        like gemini-2.5-flash-image, use /v1/chat/completions.

        Args:
          prompt: A text description of the desired image(s). The maximum length is 32000
              characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters
              for `dall-e-3`.

          background: Allows to set transparency for the background of the generated image(s). This
              parameter is only supported for `gpt-image-1`. Must be one of `transparent`,
              `opaque` or `auto` (default value). When `auto` is used, the model will
              automatically determine the best background for the image.

              If `transparent`, the output format needs to support transparency, so it should
              be set to either `png` (default value) or `webp`.

          model: The model to use for image generation. One of `openai/dall-e-2`,
              `openai/dall-e-3`, or `openai/gpt-image-1`. Defaults to `openai/dall-e-2` unless
              a parameter specific to `gpt-image-1` is used.

          moderation: Control the content-moderation level for images generated by `gpt-image-1`. Must
              be either `low` for less restrictive filtering or `auto` (default value).

          n: The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only
              `n=1` is supported.

          output_compression: The compression level (0-100%) for the generated images. This parameter is only
              supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and
              defaults to 100.

          output_format: The format in which the generated images are returned. This parameter is only
              supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.

          partial_images: The number of partial images to generate. This parameter is used for streaming
              responses that return partial images. Value must be between 0 and 3. When set to
              0, the response will be a single image sent in one streaming event.

              Note that the final image may be sent before the full number of partial images
              are generated if the full image is generated more quickly.

          quality: The quality of the image that will be generated.

              - `auto` (default value) will automatically select the best quality for the
                given model.
              - `high`, `medium` and `low` are supported for `gpt-image-1`.
              - `hd` and `standard` are supported for `dall-e-3`.
              - `standard` is the only option for `dall-e-2`.

          response_format: The format in which generated images with `dall-e-2` and `dall-e-3` are
              returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes
              after the image has been generated. This parameter isn't supported for
              `gpt-image-1` which will always return base64-encoded images.

          size: The size of the generated images. Must be one of `1024x1024`, `1536x1024`
              (landscape), `1024x1536` (portrait), or `auto` (default value) for
              `gpt-image-1`, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and
              one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.

          stream: Generate the image in streaming mode. Defaults to `false`. See the
              [Image generation guide](https://platform.openai.com/docs/guides/image-generation)
              for more information. This parameter is only supported for `gpt-image-1`.

          style: The style of the generated images. This parameter is only supported for
              `dall-e-3`. Must be one of `vivid` or `natural`. Vivid causes the model to lean
              towards generating hyper-real and dramatic images. Natural causes the model to
              produce more natural, less hyper-real looking images.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/images/generations",
            body=maybe_transform(
                {
                    "prompt": prompt,
                    "background": background,
                    "model": model,
                    "moderation": moderation,
                    "n": n,
                    "output_compression": output_compression,
                    "output_format": output_format,
                    "partial_images": partial_images,
                    "quality": quality,
                    "response_format": response_format,
                    "size": size,
                    "stream": stream,
                    "style": style,
                    "user": user,
                },
                image_generate_params.ImageGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )


class AsyncImagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncImagesResourceWithStreamingResponse(self)

    async def create_variation(
        self,
        *,
        image: FileTypes,
        model: Optional[str] | Omit = omit,
        n: Optional[int] | Omit = omit,
        response_format: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """Create variations of an image.

        DALL·E 2 only.

        Upload an image to generate variations.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v1/images/variations",
            body=await async_maybe_transform(body, image_create_variation_params.ImageCreateVariationParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )

    async def edit(
        self,
        *,
        image: FileTypes,
        prompt: str,
        mask: Optional[FileTypes] | Omit = omit,
        model: Optional[str] | Omit = omit,
        n: Optional[int] | Omit = omit,
        response_format: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """Edit images using inpainting.

        Supports dall-e-2 and gpt-image-1.

        Upload an image and optionally a mask to
        indicate which areas to regenerate based on the prompt.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        body = deepcopy_minimal(
            {
                "image": image,
                "prompt": prompt,
                "mask": mask,
                "model": model,
                "n": n,
                "response_format": response_format,
                "size": size,
                "user": user,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["image"], ["mask"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v1/images/edits",
            body=await async_maybe_transform(body, image_edit_params.ImageEditParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )

    async def generate(
        self,
        *,
        prompt: str,
        background: Optional[Literal["transparent", "opaque", "auto"]] | Omit = omit,
        model: Optional[str] | Omit = omit,
        moderation: Optional[Literal["low", "auto"]] | Omit = omit,
        n: Optional[int] | Omit = omit,
        output_compression: Optional[int] | Omit = omit,
        output_format: Optional[Literal["png", "jpeg", "webp"]] | Omit = omit,
        partial_images: Optional[int] | Omit = omit,
        quality: Optional[Literal["auto", "high", "medium", "low", "hd", "standard"]] | Omit = omit,
        response_format: Optional[Literal["url", "b64_json"]] | Omit = omit,
        size: Optional[
            Literal["256x256", "512x512", "1024x1024", "1536x1024", "1024x1536", "1792x1024", "1024x1792", "auto"]
        ]
        | Omit = omit,
        stream: Optional[bool] | Omit = omit,
        style: Optional[Literal["vivid", "natural"]] | Omit = omit,
        user: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ImagesResponse:
        """
        Generate images from text prompts.

        Pure image generation models only (DALL-E, GPT Image). For multimodal models
        like gemini-2.5-flash-image, use /v1/chat/completions.

        Args:
          prompt: A text description of the desired image(s). The maximum length is 32000
              characters for `gpt-image-1`, 1000 characters for `dall-e-2` and 4000 characters
              for `dall-e-3`.

          background: Allows to set transparency for the background of the generated image(s). This
              parameter is only supported for `gpt-image-1`. Must be one of `transparent`,
              `opaque` or `auto` (default value). When `auto` is used, the model will
              automatically determine the best background for the image.

              If `transparent`, the output format needs to support transparency, so it should
              be set to either `png` (default value) or `webp`.

          model: The model to use for image generation. One of `openai/dall-e-2`,
              `openai/dall-e-3`, or `openai/gpt-image-1`. Defaults to `openai/dall-e-2` unless
              a parameter specific to `gpt-image-1` is used.

          moderation: Control the content-moderation level for images generated by `gpt-image-1`. Must
              be either `low` for less restrictive filtering or `auto` (default value).

          n: The number of images to generate. Must be between 1 and 10. For `dall-e-3`, only
              `n=1` is supported.

          output_compression: The compression level (0-100%) for the generated images. This parameter is only
              supported for `gpt-image-1` with the `webp` or `jpeg` output formats, and
              defaults to 100.

          output_format: The format in which the generated images are returned. This parameter is only
              supported for `gpt-image-1`. Must be one of `png`, `jpeg`, or `webp`.

          partial_images: The number of partial images to generate. This parameter is used for streaming
              responses that return partial images. Value must be between 0 and 3. When set to
              0, the response will be a single image sent in one streaming event.

              Note that the final image may be sent before the full number of partial images
              are generated if the full image is generated more quickly.

          quality: The quality of the image that will be generated.

              - `auto` (default value) will automatically select the best quality for the
                given model.
              - `high`, `medium` and `low` are supported for `gpt-image-1`.
              - `hd` and `standard` are supported for `dall-e-3`.
              - `standard` is the only option for `dall-e-2`.

          response_format: The format in which generated images with `dall-e-2` and `dall-e-3` are
              returned. Must be one of `url` or `b64_json`. URLs are only valid for 60 minutes
              after the image has been generated. This parameter isn't supported for
              `gpt-image-1` which will always return base64-encoded images.

          size: The size of the generated images. Must be one of `1024x1024`, `1536x1024`
              (landscape), `1024x1536` (portrait), or `auto` (default value) for
              `gpt-image-1`, one of `256x256`, `512x512`, or `1024x1024` for `dall-e-2`, and
              one of `1024x1024`, `1792x1024`, or `1024x1792` for `dall-e-3`.

          stream: Generate the image in streaming mode. Defaults to `false`. See the
              [Image generation guide](https://platform.openai.com/docs/guides/image-generation)
              for more information. This parameter is only supported for `gpt-image-1`.

          style: The style of the generated images. This parameter is only supported for
              `dall-e-3`. Must be one of `vivid` or `natural`. Vivid causes the model to lean
              towards generating hyper-real and dramatic images. Natural causes the model to
              produce more natural, less hyper-real looking images.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices#end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/images/generations",
            body=await async_maybe_transform(
                {
                    "prompt": prompt,
                    "background": background,
                    "model": model,
                    "moderation": moderation,
                    "n": n,
                    "output_compression": output_compression,
                    "output_format": output_format,
                    "partial_images": partial_images,
                    "quality": quality,
                    "response_format": response_format,
                    "size": size,
                    "stream": stream,
                    "style": style,
                    "user": user,
                },
                image_generate_params.ImageGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ImagesResponse,
        )


class ImagesResourceWithRawResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.create_variation = to_raw_response_wrapper(
            images.create_variation,
        )
        self.edit = to_raw_response_wrapper(
            images.edit,
        )
        self.generate = to_raw_response_wrapper(
            images.generate,
        )


class AsyncImagesResourceWithRawResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.create_variation = async_to_raw_response_wrapper(
            images.create_variation,
        )
        self.edit = async_to_raw_response_wrapper(
            images.edit,
        )
        self.generate = async_to_raw_response_wrapper(
            images.generate,
        )


class ImagesResourceWithStreamingResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.create_variation = to_streamed_response_wrapper(
            images.create_variation,
        )
        self.edit = to_streamed_response_wrapper(
            images.edit,
        )
        self.generate = to_streamed_response_wrapper(
            images.generate,
        )


class AsyncImagesResourceWithStreamingResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.create_variation = async_to_streamed_response_wrapper(
            images.create_variation,
        )
        self.edit = async_to_streamed_response_wrapper(
            images.edit,
        )
        self.generate = async_to_streamed_response_wrapper(
            images.generate,
        )
