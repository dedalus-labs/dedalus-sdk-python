# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import TypeAlias

from ..._types import SequenceNotStr

__all__ = ["JSONValueInput"]

JSONValueInput: TypeAlias = Union[
    str, float, bool, Dict[str, Optional["JSONValueInput"]], SequenceNotStr[Optional["JSONValueInput"]]
]
