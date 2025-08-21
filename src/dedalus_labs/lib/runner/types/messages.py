# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Union

__all__ = [
    "Message",
]

Message = dict[str, Union[str, list[dict[str, str]]]]