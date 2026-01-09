# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..chat.input_token_details import InputTokenDetails

__all__ = [
    "TranscriptionCreateResponse",
    "CreateTranscriptionResponseVerboseJSON",
    "CreateTranscriptionResponseVerboseJSONSegment",
    "CreateTranscriptionResponseVerboseJSONUsage",
    "CreateTranscriptionResponseVerboseJSONWord",
    "CreateTranscriptionResponseJSON",
    "CreateTranscriptionResponseJSONLogprob",
    "CreateTranscriptionResponseJSONUsage",
    "CreateTranscriptionResponseJSONUsageTranscriptTextUsageTokens",
    "CreateTranscriptionResponseJSONUsageTranscriptTextUsageDuration",
]


class CreateTranscriptionResponseVerboseJSONSegment(BaseModel):
    """
    Fields:
    - id (required): int
    - seek (required): int
    - start (required): float
    - end (required): float
    - text (required): str
    - tokens (required): list[int]
    - temperature (required): float
    - avg_logprob (required): float
    - compression_ratio (required): float
    - no_speech_prob (required): float
    """

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


class CreateTranscriptionResponseVerboseJSONUsage(BaseModel):
    """Usage statistics for models billed by audio input duration."""

    seconds: float
    """Duration of the input audio in seconds."""

    type: Literal["duration"]
    """The type of the usage object. Always `duration` for this variant."""


class CreateTranscriptionResponseVerboseJSONWord(BaseModel):
    """
    Fields:
    - word (required): str
    - start (required): float
    - end (required): float
    """

    end: float
    """End time of the word in seconds."""

    start: float
    """Start time of the word in seconds."""

    word: str
    """The text content of the word."""


class CreateTranscriptionResponseVerboseJSON(BaseModel):
    """
    Represents a verbose json transcription response returned by model, based on the provided input.

    Fields:
      - language (required): str
      - duration (required): float
      - text (required): str
      - words (optional): list[TranscriptionWord]
      - segments (optional): list[TranscriptionSegment]
      - usage (optional): TranscriptTextUsageDuration
    """

    duration: float
    """The duration of the input audio."""

    language: str
    """The language of the input audio."""

    text: str
    """The transcribed text."""

    segments: Optional[List[CreateTranscriptionResponseVerboseJSONSegment]] = None
    """Segments of the transcribed text and their corresponding details."""

    usage: Optional[CreateTranscriptionResponseVerboseJSONUsage] = None
    """Usage statistics for models billed by audio input duration."""

    words: Optional[List[CreateTranscriptionResponseVerboseJSONWord]] = None
    """Extracted words and their corresponding timestamps."""


class CreateTranscriptionResponseJSONLogprob(BaseModel):
    """
    Fields:
    - token (optional): str
    - logprob (optional): float
    - bytes (optional): list[float]
    """

    token: Optional[str] = None
    """The token in the transcription."""

    bytes: Optional[List[float]] = None
    """The bytes of the token."""

    logprob: Optional[float] = None
    """The log probability of the token."""


class CreateTranscriptionResponseJSONUsageTranscriptTextUsageTokens(BaseModel):
    """Usage statistics for models billed by token usage.

    Fields:
      - type (required): Literal['tokens']
      - input_tokens (required): int
      - input_token_details (optional): InputTokenDetails
      - output_tokens (required): int
      - total_tokens (required): int
    """

    input_tokens: int
    """Number of input tokens billed for this request."""

    output_tokens: int
    """Number of output tokens generated."""

    total_tokens: int
    """Total number of tokens used (input + output)."""

    type: Literal["tokens"]
    """The type of the usage object. Always `tokens` for this variant."""

    input_token_details: Optional[InputTokenDetails] = None
    """Details about the input tokens billed for this request."""


class CreateTranscriptionResponseJSONUsageTranscriptTextUsageDuration(BaseModel):
    """Usage statistics for models billed by audio input duration.

    Fields:
      - type (required): Literal['duration']
      - seconds (required): float
    """

    seconds: float
    """Duration of the input audio in seconds."""

    type: Literal["duration"]
    """The type of the usage object. Always `duration` for this variant."""


CreateTranscriptionResponseJSONUsage: TypeAlias = Annotated[
    Union[
        CreateTranscriptionResponseJSONUsageTranscriptTextUsageTokens,
        CreateTranscriptionResponseJSONUsageTranscriptTextUsageDuration,
    ],
    PropertyInfo(discriminator="type"),
]


class CreateTranscriptionResponseJSON(BaseModel):
    """
    Represents a transcription response returned by model, based on the provided input.

    Fields:
      - text (required): str
      - logprobs (optional): list[LogprobsItem]
      - usage (optional): Usage
    """

    text: str
    """The transcribed text."""

    logprobs: Optional[List[CreateTranscriptionResponseJSONLogprob]] = None
    """The log probabilities of the tokens in the transcription.

    Only returned with the models `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`
    if `logprobs` is added to the `include` array.
    """

    usage: Optional[CreateTranscriptionResponseJSONUsage] = None
    """Token usage statistics for the request."""


TranscriptionCreateResponse: TypeAlias = Union[CreateTranscriptionResponseVerboseJSON, CreateTranscriptionResponseJSON]
