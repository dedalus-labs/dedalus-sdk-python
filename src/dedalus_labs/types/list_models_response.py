# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .model import Model
from .._models import BaseModel

__all__ = ["ListModelsResponse"]


class ListModelsResponse(BaseModel):
    data: List[Model]
    """List of available models"""

    object: Optional[Literal["list"]] = None
    """Response object type"""
