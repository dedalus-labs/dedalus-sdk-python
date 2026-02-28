# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .ocr_document_param import OCRDocumentParam

__all__ = ["OCRProcessParams"]


class OCRProcessParams(TypedDict, total=False):
    document: Required[OCRDocumentParam]
    """Document input for OCR."""

    model: str
