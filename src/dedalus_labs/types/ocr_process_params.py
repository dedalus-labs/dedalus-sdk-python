# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .ocr_document_param import OcrDocumentParam

__all__ = ["OcrProcessParams"]


class OcrProcessParams(TypedDict, total=False):
    document: Required[OcrDocumentParam]
    """Document input for OCR."""

    model: str
