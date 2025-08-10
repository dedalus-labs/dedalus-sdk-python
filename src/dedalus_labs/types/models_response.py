# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .model import Model
from .._models import BaseModel

__all__ = ["ModelsResponse"]


class ModelsResponse(BaseModel):
    data: List[Model]
    """List of models"""

    object: Optional[str] = None
    """Object type"""
