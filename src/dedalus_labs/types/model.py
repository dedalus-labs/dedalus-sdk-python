# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Model"]


class Model(BaseModel):
    id: str
    """Model identifier"""

    created: Optional[int] = None
    """Unix timestamp of model creation"""

    object: Optional[str] = None
    """Object type, always 'model'"""

    owned_by: Optional[str] = None
    """Organization that owns this model"""
