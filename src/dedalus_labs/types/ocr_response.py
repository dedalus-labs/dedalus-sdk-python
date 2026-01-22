# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .ocr_page import OcrPage

__all__ = ["OcrResponse"]


class OcrResponse(BaseModel):
    """OCR response schema."""

    model: str

    pages: List[OcrPage]

    usage: Optional[Dict[str, object]] = None
