# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-labs-python-sdk/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Callable

from .tools import JsonValue
from .messages import Message

__all__ = [
    "PolicyContext",
    "PolicyInput",
    "PolicyFunction",
]

PolicyContext = dict[str, int | list[Message] | str | list[str]]
PolicyFunction = Callable[[PolicyContext], dict[str, JsonValue]]
PolicyInput = PolicyFunction | dict[str, JsonValue] | None