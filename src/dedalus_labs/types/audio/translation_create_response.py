# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = [
    "TranslationCreateResponse",
    "CreateTranslationResponseVerboseJSON",
    "CreateTranslationResponseVerboseJSONSegment",
    "CreateTranslationResponseJSON",
]


class CreateTranslationResponseVerboseJSONSegment(BaseModel):
    id: int
    """Unique identifier of the segment."""

    avg_logprob: float
    """Average logprob of the segment.

    If the value is lower than -1, consider the logprobs failed.
    """

    compression_ratio: float
    """Compression ratio of the segment.

    If the value is greater than 2.4, consider the compression failed.
    """

    end: float
    """End time of the segment in seconds."""

    no_speech_prob: float
    """Probability of no speech in the segment.

    If the value is higher than 1.0 and the `avg_logprob` is below -1, consider this
    segment silent.
    """

    seek: int
    """Seek offset of the segment."""

    start: float
    """Start time of the segment in seconds."""

    temperature: float
    """Temperature parameter used for generating the segment."""

    text: str
    """Text content of the segment."""

    tokens: List[int]
    """Array of token IDs for the text content."""


class CreateTranslationResponseVerboseJSON(BaseModel):
    duration: float
    """The duration of the input audio."""

    language: str
    """The language of the output translation (always `english`)."""

    text: str
    """The translated text."""

    segments: Optional[List[CreateTranslationResponseVerboseJSONSegment]] = None
    """Segments of the translated text and their corresponding details."""


class CreateTranslationResponseJSON(BaseModel):
    text: str


TranslationCreateResponse: TypeAlias = Union[CreateTranslationResponseVerboseJSON, CreateTranslationResponseJSON]
