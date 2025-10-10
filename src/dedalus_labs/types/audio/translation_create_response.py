# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["TranslationCreateResponse", "Segment"]


class Segment(BaseModel):
    id: int
    """Unique identifier of the segment"""

    avg_logprob: float
    """Average log probability of the segment"""

    compression_ratio: float
    """Compression ratio of the segment.

    If greater than 2.4, consider the compression failed
    """

    end: float
    """End time of the segment in seconds"""

    no_speech_prob: float
    """Probability of no speech in the segment.

    If higher than 1.0 and avg_logprob is below -1, consider this segment silent
    """

    seek: int
    """Seek offset of the segment"""

    start: float
    """Start time of the segment in seconds"""

    temperature: float
    """Temperature parameter used for generating this segment"""

    text: str
    """Text content of the segment"""

    tokens: List[int]
    """Array of token IDs for the segment"""


class TranslationCreateResponse(BaseModel):
    text: str
    """The translated text (in English)"""

    duration: Optional[float] = None
    """The duration of the input audio in seconds"""

    language: Optional[str] = None
    """The language of the output translation (always 'english')"""

    segments: Optional[List[Segment]] = None
    """Segments of the translated text and their corresponding details"""
