# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional

from ..._models import BaseModel

__all__ = ["CredentialsBindingSpec"]


class CredentialsBindingSpec(BaseModel):
    """Detailed credential binding with options.

    Used when a binding needs default values, optional flags, or type casting.
    """

    name: str
    """Environment variable name or source identifier."""

    cast: Optional[str] = None
    """Type to cast value to (e.g., 'int', 'bool')."""

    default: Union[str, int, bool, None] = None
    """Default value if source not set."""

    optional: Optional[bool] = None
    """If true, missing value is allowed."""
