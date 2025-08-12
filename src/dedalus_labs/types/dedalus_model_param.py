# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["DedalusModelParam"]


class DedalusModelParamTyped(TypedDict, total=False):
    name: Required[str]
    """Model identifier (e.g., 'openai/gpt-4.1', 'anthropic/claude-3-5-sonnet')"""

    attributes: Optional[Dict[str, object]]
    """Model metadata for schema documentation and handoffs.

    Supports flexible types: strings, numbers, booleans, lists, dicts.
    """


DedalusModelParam: TypeAlias = Union[DedalusModelParamTyped, Dict[str, object]]
