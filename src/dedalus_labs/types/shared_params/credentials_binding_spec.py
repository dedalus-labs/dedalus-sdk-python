# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypedDict

__all__ = ["CredentialsBindingSpec"]


class CredentialsBindingSpec(TypedDict, total=False):
    """Detailed credential binding with options.

    Used when a binding needs default values, optional flags, or type casting.
    """

    name: Required[str]
    """Environment variable name or source identifier."""

    cast: Optional[str]
    """Type to cast value to (e.g., 'int', 'bool')."""

    default: Union[str, int, bool, None]
    """Default value if source not set."""

    optional: Optional[bool]
    """If true, missing value is allowed."""
