# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .top_logprob import TopLogprob

__all__ = ["ChatCompletionTokenLogprob"]


class ChatCompletionTokenLogprob(BaseModel):
    token: str
    """The token"""

    logprob: float
    """Log probability of this token"""

    top_logprobs: List[TopLogprob]
    """List of most likely tokens and their log probabilities"""

    bytes: Optional[List[int]] = None
    """Bytes representation of the token"""
