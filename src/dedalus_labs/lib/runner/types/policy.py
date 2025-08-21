# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Union, Callable

from .tools import JsonValue
from .messages import Message

__all__ = [
    "PolicyContext",
    "PolicyInput",
    "PolicyFunction",
]

PolicyContext = dict[str, Union[int, list[Message], str, list[str]]]
PolicyFunction = Callable[[PolicyContext], dict[str, JsonValue]]
PolicyInput = Union[PolicyFunction, dict[str, JsonValue], None]