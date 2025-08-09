# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .model_info import ModelInfo

__all__ = ["ModelsResponse"]


class ModelsResponse(BaseModel):
    data: List[ModelInfo]
    """List of models"""

    object: Optional[str] = None
    """Object type"""
