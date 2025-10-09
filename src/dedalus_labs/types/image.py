# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Image"]


class Image(BaseModel):
    b64_json: Optional[str] = None
    """Base64-encoded image data (if response_format=b64_json)"""

    revised_prompt: Optional[str] = None
    """Revised prompt used for generation (dall-e-3)"""

    url: Optional[str] = None
    """URL of the generated image (if response_format=url)"""
