# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import TypeAliasType

from ... import _compat

__all__ = ["JSONValueInput"]

if _compat.PYDANTIC_V1:
    # Pydantic v1 does not support recursive TypeAliasType.
    JSONValueInput = Union[str, float, bool, Dict[str, object], List[object], None]
else:
    JSONValueInput = TypeAliasType(
        "JSONValueInput",
        Union[str, float, bool, Dict[str, "JSONValueInput"], List["JSONValueInput"], None],
    )
