# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._models import FinalRequestOptions
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .lib.mcp import prepare_mcp_request, prepare_mcp_request_sync

if TYPE_CHECKING:
    from .resources import chat, audio, images, models, embeddings
    from .resources.images import ImagesResource, AsyncImagesResource
    from .resources.models import ModelsResource, AsyncModelsResource
    from .resources.chat.chat import ChatResource, AsyncChatResource
    from .resources.embeddings import EmbeddingsResource, AsyncEmbeddingsResource
    from .resources.audio.audio import AudioResource, AsyncAudioResource

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
    "development": "http://localhost:4010",
}


class Dedalus(SyncAPIClient):
    # client options
    api_key: str | None
    x_api_key: str | None
    as_base_url: str | None
    dedalus_org_id: str | None
    provider: str | None
    provider_key: str | None
    provider_model: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        as_base_url: str | None = None,
        dedalus_org_id: str | None = None,
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
        - `as_base_url` from `DEDALUS_AS_URL`
        - `dedalus_org_id` from `DEDALUS_ORG_ID`
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

        if as_base_url is None:
            as_base_url = os.environ.get("DEDALUS_AS_URL")
        self.as_base_url = as_base_url

        if dedalus_org_id is None:
            dedalus_org_id = os.environ.get("DEDALUS_ORG_ID")
        self.dedalus_org_id = dedalus_org_id

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

    @override
    def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        if options.json_data and isinstance(options.json_data, dict):
            options.json_data = prepare_mcp_request_sync(options.json_data, self.as_base_url, self._client)
        return super()._prepare_options(options)

    @cached_property
    def models(self) -> ModelsResource:
        from .resources.models import ModelsResource

        return ModelsResource(self)

    @cached_property
    def embeddings(self) -> EmbeddingsResource:
        from .resources.embeddings import EmbeddingsResource

        return EmbeddingsResource(self)

    @cached_property
    def audio(self) -> AudioResource:
        from .resources.audio import AudioResource

        return AudioResource(self)

    @cached_property
    def images(self) -> ImagesResource:
        from .resources.images import ImagesResource

        return ImagesResource(self)

    @cached_property
    def chat(self) -> ChatResource:
        from .resources.chat import ChatResource

        return ChatResource(self)

    @cached_property
    def with_raw_response(self) -> DedalusWithRawResponse:
        return DedalusWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DedalusWithStreamedResponse:
        return DedalusWithStreamedResponse(self)

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
        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        if headers.get("x-api-key") or isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            "Could not resolve authentication method. Expected either api_key or x_api_key to be set. Or for one of the `Authorization` or `x-api-key` headers to be explicitly omitted"
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        as_base_url: str | None = None,
        dedalus_org_id: str | None = None,
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
            as_base_url=as_base_url or self.as_base_url,
            dedalus_org_id=dedalus_org_id or self.dedalus_org_id,
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
    # client options
    api_key: str | None
    x_api_key: str | None
    as_base_url: str | None
    dedalus_org_id: str | None
    provider: str | None
    provider_key: str | None
    provider_model: str | None

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        as_base_url: str | None = None,
        dedalus_org_id: str | None = None,
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
        - `as_base_url` from `DEDALUS_AS_URL`
        - `dedalus_org_id` from `DEDALUS_ORG_ID`
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

        if as_base_url is None:
            as_base_url = os.environ.get("DEDALUS_AS_URL")
        self.as_base_url = as_base_url

        if dedalus_org_id is None:
            dedalus_org_id = os.environ.get("DEDALUS_ORG_ID")
        self.dedalus_org_id = dedalus_org_id

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

    @override
    async def _prepare_options(self, options: FinalRequestOptions) -> FinalRequestOptions:
        if options.json_data and isinstance(options.json_data, dict):
            options.json_data = await prepare_mcp_request(options.json_data, self.as_base_url, self._client)
        return await super()._prepare_options(options)

    @cached_property
    def models(self) -> AsyncModelsResource:
        from .resources.models import AsyncModelsResource

        return AsyncModelsResource(self)

    @cached_property
    def embeddings(self) -> AsyncEmbeddingsResource:
        from .resources.embeddings import AsyncEmbeddingsResource

        return AsyncEmbeddingsResource(self)

    @cached_property
    def audio(self) -> AsyncAudioResource:
        from .resources.audio import AsyncAudioResource

        return AsyncAudioResource(self)

    @cached_property
    def images(self) -> AsyncImagesResource:
        from .resources.images import AsyncImagesResource

        return AsyncImagesResource(self)

    @cached_property
    def chat(self) -> AsyncChatResource:
        from .resources.chat import AsyncChatResource

        return AsyncChatResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncDedalusWithRawResponse:
        return AsyncDedalusWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDedalusWithStreamedResponse:
        return AsyncDedalusWithStreamedResponse(self)

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
        if headers.get("Authorization") or isinstance(custom_headers.get("Authorization"), Omit):
            return

        if headers.get("x-api-key") or isinstance(custom_headers.get("x-api-key"), Omit):
            return

        raise TypeError(
            "Could not resolve authentication method. Expected either api_key or x_api_key to be set. Or for one of the `Authorization` or `x-api-key` headers to be explicitly omitted"
        )

    def copy(
        self,
        *,
        api_key: str | None = None,
        x_api_key: str | None = None,
        as_base_url: str | None = None,
        dedalus_org_id: str | None = None,
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
            as_base_url=as_base_url or self.as_base_url,
            dedalus_org_id=dedalus_org_id or self.dedalus_org_id,
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
    _client: Dedalus

    def __init__(self, client: Dedalus) -> None:
        self._client = client

    @cached_property
    def models(self) -> models.ModelsResourceWithRawResponse:
        from .resources.models import ModelsResourceWithRawResponse

        return ModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def embeddings(self) -> embeddings.EmbeddingsResourceWithRawResponse:
        from .resources.embeddings import EmbeddingsResourceWithRawResponse

        return EmbeddingsResourceWithRawResponse(self._client.embeddings)

    @cached_property
    def audio(self) -> audio.AudioResourceWithRawResponse:
        from .resources.audio import AudioResourceWithRawResponse

        return AudioResourceWithRawResponse(self._client.audio)

    @cached_property
    def images(self) -> images.ImagesResourceWithRawResponse:
        from .resources.images import ImagesResourceWithRawResponse

        return ImagesResourceWithRawResponse(self._client.images)

    @cached_property
    def chat(self) -> chat.ChatResourceWithRawResponse:
        from .resources.chat import ChatResourceWithRawResponse

        return ChatResourceWithRawResponse(self._client.chat)


class AsyncDedalusWithRawResponse:
    _client: AsyncDedalus

    def __init__(self, client: AsyncDedalus) -> None:
        self._client = client

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithRawResponse:
        from .resources.models import AsyncModelsResourceWithRawResponse

        return AsyncModelsResourceWithRawResponse(self._client.models)

    @cached_property
    def embeddings(self) -> embeddings.AsyncEmbeddingsResourceWithRawResponse:
        from .resources.embeddings import AsyncEmbeddingsResourceWithRawResponse

        return AsyncEmbeddingsResourceWithRawResponse(self._client.embeddings)

    @cached_property
    def audio(self) -> audio.AsyncAudioResourceWithRawResponse:
        from .resources.audio import AsyncAudioResourceWithRawResponse

        return AsyncAudioResourceWithRawResponse(self._client.audio)

    @cached_property
    def images(self) -> images.AsyncImagesResourceWithRawResponse:
        from .resources.images import AsyncImagesResourceWithRawResponse

        return AsyncImagesResourceWithRawResponse(self._client.images)

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithRawResponse:
        from .resources.chat import AsyncChatResourceWithRawResponse

        return AsyncChatResourceWithRawResponse(self._client.chat)


class DedalusWithStreamedResponse:
    _client: Dedalus

    def __init__(self, client: Dedalus) -> None:
        self._client = client

    @cached_property
    def models(self) -> models.ModelsResourceWithStreamingResponse:
        from .resources.models import ModelsResourceWithStreamingResponse

        return ModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def embeddings(self) -> embeddings.EmbeddingsResourceWithStreamingResponse:
        from .resources.embeddings import EmbeddingsResourceWithStreamingResponse

        return EmbeddingsResourceWithStreamingResponse(self._client.embeddings)

    @cached_property
    def audio(self) -> audio.AudioResourceWithStreamingResponse:
        from .resources.audio import AudioResourceWithStreamingResponse

        return AudioResourceWithStreamingResponse(self._client.audio)

    @cached_property
    def images(self) -> images.ImagesResourceWithStreamingResponse:
        from .resources.images import ImagesResourceWithStreamingResponse

        return ImagesResourceWithStreamingResponse(self._client.images)

    @cached_property
    def chat(self) -> chat.ChatResourceWithStreamingResponse:
        from .resources.chat import ChatResourceWithStreamingResponse

        return ChatResourceWithStreamingResponse(self._client.chat)


class AsyncDedalusWithStreamedResponse:
    _client: AsyncDedalus

    def __init__(self, client: AsyncDedalus) -> None:
        self._client = client

    @cached_property
    def models(self) -> models.AsyncModelsResourceWithStreamingResponse:
        from .resources.models import AsyncModelsResourceWithStreamingResponse

        return AsyncModelsResourceWithStreamingResponse(self._client.models)

    @cached_property
    def embeddings(self) -> embeddings.AsyncEmbeddingsResourceWithStreamingResponse:
        from .resources.embeddings import AsyncEmbeddingsResourceWithStreamingResponse

        return AsyncEmbeddingsResourceWithStreamingResponse(self._client.embeddings)

    @cached_property
    def audio(self) -> audio.AsyncAudioResourceWithStreamingResponse:
        from .resources.audio import AsyncAudioResourceWithStreamingResponse

        return AsyncAudioResourceWithStreamingResponse(self._client.audio)

    @cached_property
    def images(self) -> images.AsyncImagesResourceWithStreamingResponse:
        from .resources.images import AsyncImagesResourceWithStreamingResponse

        return AsyncImagesResourceWithStreamingResponse(self._client.images)

    @cached_property
    def chat(self) -> chat.AsyncChatResourceWithStreamingResponse:
        from .resources.chat import AsyncChatResourceWithStreamingResponse

        return AsyncChatResourceWithStreamingResponse(self._client.chat)


Client = Dedalus

AsyncClient = AsyncDedalus
