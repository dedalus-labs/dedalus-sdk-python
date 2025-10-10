# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Dict, List, Union, Callable

from .tools import JsonValue
from .messages import Message

__all__ = [
    "PolicyContext",
    "PolicyInput",
    "PolicyFunction",
]

PolicyContext = Dict[str, Union[int, List[Message], str, List[str]]]
PolicyFunction = Callable[[PolicyContext], Dict[str, JsonValue]]
PolicyInput = Union[PolicyFunction, Dict[str, JsonValue], None]
