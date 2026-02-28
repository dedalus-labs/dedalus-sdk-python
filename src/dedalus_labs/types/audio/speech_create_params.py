# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..shared_params.voice_ids_or_custom_voice import VoiceIDsOrCustomVoice

__all__ = ["SpeechCreateParams", "Voice"]


class SpeechCreateParams(TypedDict, total=False):
    input: Required[str]
    """The text to generate audio for. The maximum length is 4096 characters."""

    model: Required[Union[str, Literal["tts-1", "tts-1-hd", "gpt-4o-mini-tts", "gpt-4o-mini-tts-2025-12-15"]]]
    """
    One of the available [TTS models](/docs/models#tts): `tts-1`, `tts-1-hd`,
    `gpt-4o-mini-tts`, or `gpt-4o-mini-tts-2025-12-15`.
    """

    voice: Required[Voice]
    """The voice to use when generating the audio.

    Supported built-in voices are `alloy`, `ash`, `ballad`, `coral`, `echo`,
    `fable`, `onyx`, `nova`, `sage`, `shimmer`, `verse`, `marin`, and `cedar`. You
    may also provide a custom voice object with an `id`, for example
    `{ "id": "voice_1234" }`. Previews of the voices are available in the
    [Text to speech guide](/docs/guides/text-to-speech#voice-options).
    """

    instructions: str
    """Control the voice of your generated audio with additional instructions.

    Does not work with `tts-1` or `tts-1-hd`.
    """

    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]
    """The format to audio in.

    Supported formats are `mp3`, `opus`, `aac`, `flac`, `wav`, and `pcm`.
    """

    speed: float
    """The speed of the generated audio.

    Select a value from `0.25` to `4.0`. `1.0` is the default.
    """

    stream_format: Literal["sse", "audio"]
    """The format to stream the audio in.

    Supported formats are `sse` and `audio`. `sse` is not supported for `tts-1` or
    `tts-1-hd`.
    """


Voice: TypeAlias = Union[
    str,
    Literal["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse", "marin", "cedar"],
    VoiceIDsOrCustomVoice,
]
