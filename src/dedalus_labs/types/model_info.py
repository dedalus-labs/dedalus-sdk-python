# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import List, Optional

from .._models import BaseModel

__all__ = ["ModelInfo"]


class ModelInfo(BaseModel):
    id: str
    """Model identifier"""

    created: Optional[int] = None
    """Creation timestamp"""

    object: Optional[str] = None
    """Object type"""

    owned_by: Optional[str] = None
    """Model owner"""

    parent: Optional[str] = None
    """Parent model"""

    permission: Optional[List[builtins.object]] = None
    """Permissions"""

    root: Optional[str] = None
    """Root model"""
