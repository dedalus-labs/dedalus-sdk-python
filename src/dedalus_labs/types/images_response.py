# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .image import Image
from .._models import BaseModel

__all__ = ["ImagesResponse"]


class ImagesResponse(BaseModel):
    created: int
    """Unix timestamp when images were created"""

    data: List[Image]
    """List of generated images"""
