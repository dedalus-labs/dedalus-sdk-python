# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel
from .ocr_page import OCRPage

__all__ = ["OCRResponse"]


class OCRResponse(BaseModel):
    """OCR response schema."""

    model: str

    pages: List[OCRPage]

    usage: Optional[Dict[str, object]] = None
