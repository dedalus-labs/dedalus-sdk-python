# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["OCRPage"]


class OCRPage(BaseModel):
    """Single page OCR result."""

    index: int

    markdown: str
