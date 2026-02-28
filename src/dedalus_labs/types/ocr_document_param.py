# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["OCRDocumentParam"]


class OCRDocumentParam(TypedDict, total=False):
    """Document input for OCR."""

    document_url: Required[str]
    """Data URI with base64-encoded document"""

    type: str
