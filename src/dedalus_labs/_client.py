# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .resources import health, images, models, embeddings
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .resources.chat import chat
from .resources.audio import audio
from .types.get_response import GetResponse

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Dedalus",
    "AsyncDedalus",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://api.dedaluslabs.ai",
    "development": "http://localhost:8080",
}


class Dedalus(SyncAPIClient):
    health: health.HealthResource
    models: models.ModelsResource
    embeddings: embeddings.EmbeddingsResource
    audio: audio.AudioResource
    images: images.ImagesResource
    chat: chat.ChatResource
    with_raw_response: DedalusWithRawResponse
    with_streaming_response: DedalusWithStreamedResponse

    # client options
    api_key: str | None
    x_api_key: str | None
    organization: str | None
    provider: str | None
    provider_key: str | None
    provider_model: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        organization: str | None = None,
        provider: str | None = None,
        provider_key: str | None = None,
        provider_model: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Dedalus client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `DEDALUS_API_KEY`
        - `x_api_key` from `DEDALUS_X_API_KEY`
        - `organization` from `DEDALUS_ORG_ID`
        - `provider` from `DEDALUS_PROVIDER`
        - `provider_key` from `DEDALUS_PROVIDER_KEY`
        - `provider_model` from `DEDALUS_PROVIDER_MODEL`
        """
        if api_key is None:
            api_key = os.environ.get("DEDALUS_API_KEY")
        self.api_key = api_key

        if x_api_key is None:
            x_api_key = os.environ.get("DEDALUS_X_API_KEY")
        self.x_api_key = x_api_key

        if organization is None:
            organization = os.environ.get("DEDALUS_ORG_ID")
        self.organization = organization

        if provider is None:
            provider = os.environ.get("DEDALUS_PROVIDER")
        self.provider = provider

        if provider_key is None:
            provider_key = os.environ.get("DEDALUS_PROVIDER_KEY")
        self.provider_key = provider_key

        if provider_model is None:
            provider_model = os.environ.get("DEDALUS_PROVIDER_MODEL")
        self.provider_model = provider_model

        self._environment = environment

        base_url_env = os.environ.get("DEDALUS_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `DEDALUS_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "Idempotency-Key"

        self._default_stream_cls = Stream

        self.health = health.HealthResource(self)
        self.models = models.ModelsResource(self)
        self.embeddings = embeddings.EmbeddingsResource(self)
        self.audio = audio.AudioResource(self)
        self.images = images.ImagesResource(self)
        self.chat = chat.ChatResource(self)
        self.with_raw_response = DedalusWithRawResponse(self)
        self.with_streaming_response = DedalusWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._bearer, **self._api_key_auth}

    @property
    def _bearer(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        x_api_key = self.x_api_key
        if x_api_key is None:
            return {}
        return {"x-api-key": x_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "User-Agent": "Dedalus-SDK",
            "X-SDK-Version": "1.0.0",
            "X-Provider": self.provider if self.provider is not None else Omit(),
            "X-Provider-Key": self.provider_key if self.provider_key is not None else Omit(),
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.x_api_key and headers.get("x-api-key"):
            return
        if isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or x_api_key to be set. Or for one of the `Authorization` or `x-api-key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        organization: str | None = None,
        provider: str | None = None,
        provider_key: str | None = None,
        provider_model: str | None = None,
        environment: Literal["production", "development"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            x_api_key=x_api_key or self.x_api_key,
            organization=organization or self.organization,
            provider=provider or self.provider,
            provider_key=provider_key or self.provider_key,
            provider_model=provider_model or self.provider_model,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GetResponse:
        """Root"""
        return self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GetResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncDedalus(AsyncAPIClient):
    health: health.AsyncHealthResource
    models: models.AsyncModelsResource
    embeddings: embeddings.AsyncEmbeddingsResource
    audio: audio.AsyncAudioResource
    images: images.AsyncImagesResource
    chat: chat.AsyncChatResource
    with_raw_response: AsyncDedalusWithRawResponse
    with_streaming_response: AsyncDedalusWithStreamedResponse

    # client options
    api_key: str | None
    x_api_key: str | None
    organization: str | None
    provider: str | None
    provider_key: str | None
    provider_model: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        organization: str | None = None,
        provider: str | None = None,
        provider_key: str | None = None,
        provider_model: str | None = None,
        environment: Literal["production", "development"] | NotGiven = not_given,
        base_url: str | httpx.URL | None | NotGiven = not_given,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncDedalus client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `DEDALUS_API_KEY`
        - `x_api_key` from `DEDALUS_X_API_KEY`
        - `organization` from `DEDALUS_ORG_ID`
        - `provider` from `DEDALUS_PROVIDER`
        - `provider_key` from `DEDALUS_PROVIDER_KEY`
        - `provider_model` from `DEDALUS_PROVIDER_MODEL`
        """
        if api_key is None:
            api_key = os.environ.get("DEDALUS_API_KEY")
        self.api_key = api_key

        if x_api_key is None:
            x_api_key = os.environ.get("DEDALUS_X_API_KEY")
        self.x_api_key = x_api_key

        if organization is None:
            organization = os.environ.get("DEDALUS_ORG_ID")
        self.organization = organization

        if provider is None:
            provider = os.environ.get("DEDALUS_PROVIDER")
        self.provider = provider

        if provider_key is None:
            provider_key = os.environ.get("DEDALUS_PROVIDER_KEY")
        self.provider_key = provider_key

        if provider_model is None:
            provider_model = os.environ.get("DEDALUS_PROVIDER_MODEL")
        self.provider_model = provider_model

        self._environment = environment

        base_url_env = os.environ.get("DEDALUS_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `DEDALUS_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "Idempotency-Key"

        self._default_stream_cls = AsyncStream

        self.health = health.AsyncHealthResource(self)
        self.models = models.AsyncModelsResource(self)
        self.embeddings = embeddings.AsyncEmbeddingsResource(self)
        self.audio = audio.AsyncAudioResource(self)
        self.images = images.AsyncImagesResource(self)
        self.chat = chat.AsyncChatResource(self)
        self.with_raw_response = AsyncDedalusWithRawResponse(self)
        self.with_streaming_response = AsyncDedalusWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._bearer, **self._api_key_auth}

    @property
    def _bearer(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        x_api_key = self.x_api_key
        if x_api_key is None:
            return {}
        return {"x-api-key": x_api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "User-Agent": "Dedalus-SDK",
            "X-SDK-Version": "1.0.0",
            "X-Provider": self.provider if self.provider is not None else Omit(),
            "X-Provider-Key": self.provider_key if self.provider_key is not None else Omit(),
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.x_api_key and headers.get("x-api-key"):
            return
        if isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either api_key or x_api_key to be set. Or for one of the `Authorization` or `x-api-key` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        organization: str | None = None,
        provider: str | None = None,
        provider_key: str | None = None,
        provider_model: str | None = None,
        environment: Literal["production", "development"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            x_api_key=x_api_key or self.x_api_key,
            organization=organization or self.organization,
            provider=provider or self.provider,
            provider_key=provider_key or self.provider_key,
            provider_model=provider_model or self.provider_model,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GetResponse:
        """Root"""
        return await self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GetResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class DedalusWithRawResponse:
    def __init__(self, client: Dedalus) -> None:
        self.health = health.HealthResourceWithRawResponse(client.health)
        self.models = models.ModelsResourceWithRawResponse(client.models)
        self.embeddings = embeddings.EmbeddingsResourceWithRawResponse(client.embeddings)
        self.audio = audio.AudioResourceWithRawResponse(client.audio)
        self.images = images.ImagesResourceWithRawResponse(client.images)
        self.chat = chat.ChatResourceWithRawResponse(client.chat)

        self.get = to_raw_response_wrapper(
            client.get,
        )


class AsyncDedalusWithRawResponse:
    def __init__(self, client: AsyncDedalus) -> None:
        self.health = health.AsyncHealthResourceWithRawResponse(client.health)
        self.models = models.AsyncModelsResourceWithRawResponse(client.models)
        self.embeddings = embeddings.AsyncEmbeddingsResourceWithRawResponse(client.embeddings)
        self.audio = audio.AsyncAudioResourceWithRawResponse(client.audio)
        self.images = images.AsyncImagesResourceWithRawResponse(client.images)
        self.chat = chat.AsyncChatResourceWithRawResponse(client.chat)

        self.get = async_to_raw_response_wrapper(
            client.get,
        )


class DedalusWithStreamedResponse:
    def __init__(self, client: Dedalus) -> None:
        self.health = health.HealthResourceWithStreamingResponse(client.health)
        self.models = models.ModelsResourceWithStreamingResponse(client.models)
        self.embeddings = embeddings.EmbeddingsResourceWithStreamingResponse(client.embeddings)
        self.audio = audio.AudioResourceWithStreamingResponse(client.audio)
        self.images = images.ImagesResourceWithStreamingResponse(client.images)
        self.chat = chat.ChatResourceWithStreamingResponse(client.chat)

        self.get = to_streamed_response_wrapper(
            client.get,
        )


class AsyncDedalusWithStreamedResponse:
    def __init__(self, client: AsyncDedalus) -> None:
        self.health = health.AsyncHealthResourceWithStreamingResponse(client.health)
        self.models = models.AsyncModelsResourceWithStreamingResponse(client.models)
        self.embeddings = embeddings.AsyncEmbeddingsResourceWithStreamingResponse(client.embeddings)
        self.audio = audio.AsyncAudioResourceWithStreamingResponse(client.audio)
        self.images = images.AsyncImagesResourceWithStreamingResponse(client.images)
        self.chat = chat.AsyncChatResourceWithStreamingResponse(client.chat)

        self.get = async_to_streamed_response_wrapper(
            client.get,
        )


Client = Dedalus

AsyncClient = AsyncDedalus
