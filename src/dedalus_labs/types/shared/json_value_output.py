# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import TypeAliasType

__all__ = ["JSONValueOutput"]

JSONValueOutput = TypeAliasType(
    "JSONValueOutput",
    Union[str, float, bool, Dict[str, Optional["JSONValueOutput"]], List[Optional["JSONValueOutput"]], None],
)
