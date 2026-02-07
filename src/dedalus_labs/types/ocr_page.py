# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["OcrPage"]


class OcrPage(BaseModel):
    """Single page OCR result."""

    index: int

    markdown: str
