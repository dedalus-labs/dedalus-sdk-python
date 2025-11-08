# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Dict, List, Union

__all__ = [
    "Message",
]

Message = Dict[str, Union[str, List[Dict[str, str]]]]
