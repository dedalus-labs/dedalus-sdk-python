# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["PromptTokensDetails"]


class PromptTokensDetails(BaseModel):
    """Breakdown of tokens used in the prompt.

    Fields:
    - audio_tokens (optional): int
    - cached_tokens (optional): int
    """

    audio_tokens: Optional[int] = None
    """Audio input tokens present in the prompt."""

    cached_tokens: Optional[int] = None
    """Cached tokens present in the prompt."""
