# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["PromptTokensDetails"]


class PromptTokensDetails(BaseModel):
    audio_tokens: Optional[int] = None
    """Audio input tokens present in the prompt."""

    cached_tokens: Optional[int] = None
    """Cached tokens present in the prompt."""
