# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..shared_params.voice_ids_or_custom_voice import VoiceIDsOrCustomVoice

__all__ = ["ChatCompletionAudioParam", "Voice"]

Voice: TypeAlias = Union[
    str,
    Literal["alloy", "ash", "ballad", "coral", "echo", "sage", "shimmer", "verse", "marin", "cedar"],
    VoiceIDsOrCustomVoice,
]


class ChatCompletionAudioParam(TypedDict, total=False):
    """Parameters for audio output.

    Required when audio output is requested with
    `modalities: ["audio"]`. [Learn more](/docs/guides/audio).

    Fields:
    - voice (required): VoiceIdsOrCustomVoice
    - format (required): Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]
    """

    format: Required[Literal["wav", "aac", "mp3", "flac", "opus", "pcm16"]]
    """Specifies the output audio format.

    Must be one of `wav`, `mp3`, `flac`, `opus`, or `pcm16`.
    """

    voice: Required[Voice]
    """The voice the model uses to respond.

    Supported built-in voices are `alloy`, `ash`, `ballad`, `coral`, `echo`,
    `fable`, `nova`, `onyx`, `sage`, `shimmer`, `marin`, and `cedar`. You may also
    provide a custom voice object with an `id`, for example
    `{ "id": "voice_1234" }`.
    """
