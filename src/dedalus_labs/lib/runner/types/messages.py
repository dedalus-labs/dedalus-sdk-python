# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-labs-python-sdk/LICENSE
# ==============================================================================

from __future__ import annotations

__all__ = [
    "Message",
]

Message = dict[str, str | list[dict[str, str]]]