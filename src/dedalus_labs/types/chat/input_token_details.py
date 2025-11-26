# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["InputTokenDetails"]


class InputTokenDetails(BaseModel):
    audio_tokens: Optional[int] = None
    """Number of audio tokens billed for this request."""

    text_tokens: Optional[int] = None
    """Number of text tokens billed for this request."""
