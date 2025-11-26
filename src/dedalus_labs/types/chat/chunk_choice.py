# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .choice_delta import ChoiceDelta
from .choice_logprobs import ChoiceLogprobs

__all__ = ["ChunkChoice"]


class ChunkChoice(BaseModel):
    delta: ChoiceDelta
    """Delta content for streaming responses"""

    index: int
    """The index of this choice in the list of choices"""

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
    """The reason the model stopped (only in final chunk)"""

    logprobs: Optional[ChoiceLogprobs] = None
    """Log probability information for the choice."""
