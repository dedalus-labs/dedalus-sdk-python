# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import TypeAliasType

__all__ = ["JSONValueInput"]

JSONValueInput = TypeAliasType(
    "JSONValueInput",
    Union[str, float, bool, Dict[str, Optional["JSONValueInput"]], List[Optional["JSONValueInput"]], None],
)
