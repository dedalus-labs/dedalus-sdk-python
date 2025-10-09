# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .speech import (
    SpeechResource,
    AsyncSpeechResource,
    SpeechResourceWithRawResponse,
    AsyncSpeechResourceWithRawResponse,
    SpeechResourceWithStreamingResponse,
    AsyncSpeechResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .translations import (
    TranslationsResource,
    AsyncTranslationsResource,
    TranslationsResourceWithRawResponse,
    AsyncTranslationsResourceWithRawResponse,
    TranslationsResourceWithStreamingResponse,
    AsyncTranslationsResourceWithStreamingResponse,
)
from .transcriptions import (
    TranscriptionsResource,
    AsyncTranscriptionsResource,
    TranscriptionsResourceWithRawResponse,
    AsyncTranscriptionsResourceWithRawResponse,
    TranscriptionsResourceWithStreamingResponse,
    AsyncTranscriptionsResourceWithStreamingResponse,
)

__all__ = ["AudioResource", "AsyncAudioResource"]


class AudioResource(SyncAPIResource):
    @cached_property
    def speech(self) -> SpeechResource:
        return SpeechResource(self._client)

    @cached_property
    def transcriptions(self) -> TranscriptionsResource:
        return TranscriptionsResource(self._client)

    @cached_property
    def translations(self) -> TranslationsResource:
        return TranslationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AudioResourceWithStreamingResponse(self)


class AsyncAudioResource(AsyncAPIResource):
    @cached_property
    def speech(self) -> AsyncSpeechResource:
        return AsyncSpeechResource(self._client)

    @cached_property
    def transcriptions(self) -> AsyncTranscriptionsResource:
        return AsyncTranscriptionsResource(self._client)

    @cached_property
    def translations(self) -> AsyncTranslationsResource:
        return AsyncTranslationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dedalus-labs/dedalus-sdk-python#with_streaming_response
        """
        return AsyncAudioResourceWithStreamingResponse(self)


class AudioResourceWithRawResponse:
    def __init__(self, audio: AudioResource) -> None:
        self._audio = audio

    @cached_property
    def speech(self) -> SpeechResourceWithRawResponse:
        return SpeechResourceWithRawResponse(self._audio.speech)

    @cached_property
    def transcriptions(self) -> TranscriptionsResourceWithRawResponse:
        return TranscriptionsResourceWithRawResponse(self._audio.transcriptions)

    @cached_property
    def translations(self) -> TranslationsResourceWithRawResponse:
        return TranslationsResourceWithRawResponse(self._audio.translations)


class AsyncAudioResourceWithRawResponse:
    def __init__(self, audio: AsyncAudioResource) -> None:
        self._audio = audio

    @cached_property
    def speech(self) -> AsyncSpeechResourceWithRawResponse:
        return AsyncSpeechResourceWithRawResponse(self._audio.speech)

    @cached_property
    def transcriptions(self) -> AsyncTranscriptionsResourceWithRawResponse:
        return AsyncTranscriptionsResourceWithRawResponse(self._audio.transcriptions)

    @cached_property
    def translations(self) -> AsyncTranslationsResourceWithRawResponse:
        return AsyncTranslationsResourceWithRawResponse(self._audio.translations)


class AudioResourceWithStreamingResponse:
    def __init__(self, audio: AudioResource) -> None:
        self._audio = audio

    @cached_property
    def speech(self) -> SpeechResourceWithStreamingResponse:
        return SpeechResourceWithStreamingResponse(self._audio.speech)

    @cached_property
    def transcriptions(self) -> TranscriptionsResourceWithStreamingResponse:
        return TranscriptionsResourceWithStreamingResponse(self._audio.transcriptions)

    @cached_property
    def translations(self) -> TranslationsResourceWithStreamingResponse:
        return TranslationsResourceWithStreamingResponse(self._audio.translations)


class AsyncAudioResourceWithStreamingResponse:
    def __init__(self, audio: AsyncAudioResource) -> None:
        self._audio = audio

    @cached_property
    def speech(self) -> AsyncSpeechResourceWithStreamingResponse:
        return AsyncSpeechResourceWithStreamingResponse(self._audio.speech)

    @cached_property
    def transcriptions(self) -> AsyncTranscriptionsResourceWithStreamingResponse:
        return AsyncTranscriptionsResourceWithStreamingResponse(self._audio.transcriptions)

    @cached_property
    def translations(self) -> AsyncTranslationsResourceWithStreamingResponse:
        return AsyncTranslationsResourceWithStreamingResponse(self._audio.translations)
