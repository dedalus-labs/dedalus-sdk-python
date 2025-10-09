# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..._types import FileTypes

__all__ = ["TranscriptionCreateParams"]


class TranscriptionCreateParams(TypedDict, total=False):
    file: Required[FileTypes]

    model: Required[str]

    language: Optional[str]

    prompt: Optional[str]

    response_format: Optional[str]

    temperature: Optional[float]
