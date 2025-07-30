# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["Model"]


class Model(BaseModel):
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

    permission: Optional[List[Dict[str, builtins.object]]] = None
    """Permissions"""

    root: Optional[str] = None
    """Root model"""
