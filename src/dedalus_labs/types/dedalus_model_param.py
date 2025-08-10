# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["DedalusModelParam"]


class DedalusModelParam(TypedDict, total=False):
    name: Required[str]
    """Model identifier (e.g., 'gpt-4', 'claude-3-sonnet')"""

    attributes: Optional[Dict[str, object]]
    """Model metadata for schema documentation and handoffs.

    Supports flexible types: strings, numbers, booleans, lists, dicts.
    """
