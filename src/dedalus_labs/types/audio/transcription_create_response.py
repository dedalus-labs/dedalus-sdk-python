# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "TranscriptionCreateResponse",
    "CreateTranscriptionResponseVerboseJson",
    "CreateTranscriptionResponseVerboseJsonSegment",
    "CreateTranscriptionResponseVerboseJsonUsage",
    "CreateTranscriptionResponseVerboseJsonWord",
    "CreateTranscriptionResponseJson",
    "CreateTranscriptionResponseJsonLogprob",
    "CreateTranscriptionResponseJsonUsage",
    "CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokens",
    "CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokensInputTokenDetails",
    "CreateTranscriptionResponseJsonUsageTranscriptTextUsageDuration",
]


class CreateTranscriptionResponseVerboseJsonSegment(BaseModel):
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


class CreateTranscriptionResponseVerboseJsonUsage(BaseModel):
    seconds: float
    """Duration of the input audio in seconds."""

    type: Literal["duration"]
    """The type of the usage object. Always `duration` for this variant."""


class CreateTranscriptionResponseVerboseJsonWord(BaseModel):
    end: float
    """End time of the word in seconds."""

    start: float
    """Start time of the word in seconds."""

    word: str
    """The text content of the word."""


class CreateTranscriptionResponseVerboseJson(BaseModel):
    duration: float
    """The duration of the input audio."""

    language: str
    """The language of the input audio."""

    text: str
    """The transcribed text."""

    segments: Optional[List[CreateTranscriptionResponseVerboseJsonSegment]] = None
    """Segments of the transcribed text and their corresponding details."""

    usage: Optional[CreateTranscriptionResponseVerboseJsonUsage] = None
    """Usage statistics for models billed by audio input duration."""

    words: Optional[List[CreateTranscriptionResponseVerboseJsonWord]] = None
    """Extracted words and their corresponding timestamps."""


class CreateTranscriptionResponseJsonLogprob(BaseModel):
    token: Optional[str] = None
    """The token in the transcription."""

    bytes: Optional[List[float]] = None
    """The bytes of the token."""

    logprob: Optional[float] = None
    """The log probability of the token."""


class CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokensInputTokenDetails(BaseModel):
    audio_tokens: Optional[int] = None
    """Number of audio tokens billed for this request."""

    text_tokens: Optional[int] = None
    """Number of text tokens billed for this request."""


class CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokens(BaseModel):
    input_tokens: int
    """Number of input tokens billed for this request."""

    output_tokens: int
    """Number of output tokens generated."""

    total_tokens: int
    """Total number of tokens used (input + output)."""

    type: Literal["tokens"]
    """The type of the usage object. Always `tokens` for this variant."""

    input_token_details: Optional[CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokensInputTokenDetails] = None
    """Details about the input tokens billed for this request."""


class CreateTranscriptionResponseJsonUsageTranscriptTextUsageDuration(BaseModel):
    seconds: float
    """Duration of the input audio in seconds."""

    type: Literal["duration"]
    """The type of the usage object. Always `duration` for this variant."""


CreateTranscriptionResponseJsonUsage: TypeAlias = Annotated[
    Union[
        CreateTranscriptionResponseJsonUsageTranscriptTextUsageTokens,
        CreateTranscriptionResponseJsonUsageTranscriptTextUsageDuration,
    ],
    PropertyInfo(discriminator="type"),
]


class CreateTranscriptionResponseJson(BaseModel):
    text: str
    """The transcribed text."""

    logprobs: Optional[List[CreateTranscriptionResponseJsonLogprob]] = None
    """The log probabilities of the tokens in the transcription.

    Only returned with the models `gpt-4o-transcribe` and `gpt-4o-mini-transcribe`
    if `logprobs` is added to the `include` array.
    """

    usage: Optional[CreateTranscriptionResponseJsonUsage] = None
    """Token usage statistics for the request."""


TranscriptionCreateResponse: TypeAlias = Union[CreateTranscriptionResponseVerboseJson, CreateTranscriptionResponseJson]
