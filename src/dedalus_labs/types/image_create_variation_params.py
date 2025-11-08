# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["ImageCreateVariationParams"]


class ImageCreateVariationParams(TypedDict, total=False):
    image: Required[FileTypes]

    model: Optional[str]

    n: Optional[int]

    response_format: Optional[str]

    size: Optional[str]

    user: Optional[str]
