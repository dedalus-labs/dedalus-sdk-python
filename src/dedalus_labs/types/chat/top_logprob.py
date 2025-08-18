# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["TopLogprob"]


class TopLogprob(BaseModel):
    token: str
    """The token"""

    logprob: float
    """Log probability of this token"""

    bytes: Optional[List[int]] = None
    """Bytes representation of the token"""
