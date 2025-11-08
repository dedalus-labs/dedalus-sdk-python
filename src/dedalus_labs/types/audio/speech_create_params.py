# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["SpeechCreateParams"]


class SpeechCreateParams(TypedDict, total=False):
    input: Required[str]
    """The text to generate audio for. The maximum length is 4096 characters."""

    model: Required[str]
    """
    One of the available [TTS models](https://platform.openai.com/docs/models#tts):
    `openai/tts-1`, `openai/tts-1-hd` or `openai/gpt-4o-mini-tts`.
    """

    voice: Required[
        Literal["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
    ]
    """The voice to use when generating the audio.

    Supported voices are `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `onyx`,
    `nova`, `sage`, `shimmer`, and `verse`. Previews of the voices are available in
    the
    [Text to speech guide](https://platform.openai.com/docs/guides/text-to-speech#voice-options).
    """

    instructions: Optional[str]
    """Control the voice of your generated audio with additional instructions.

    Does not work with `tts-1` or `tts-1-hd`.
    """

    response_format: Optional[Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]]
    """The format to audio in.

    Supported formats are `mp3`, `opus`, `aac`, `flac`, `wav`, and `pcm`.
    """

    speed: Optional[float]
    """The speed of the generated audio.

    Select a value from `0.25` to `4.0`. `1.0` is the default.
    """

    stream_format: Optional[Literal["sse", "audio"]]
    """The format to stream the audio in.

    Supported formats are `sse` and `audio`. `sse` is not supported for `tts-1` or
    `tts-1-hd`.
    """
