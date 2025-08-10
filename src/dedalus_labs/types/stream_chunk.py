# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import TYPE_CHECKING, Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["StreamChunk"]


class StreamChunk(BaseModel):
    id: str

    choices: List[object]

    created: int

    model: str

    object: Literal["chat.completion.chunk"]

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    system_fingerprint: Optional[str] = None

    usage: Optional[builtins.object] = None

    __pydantic_extra__: Dict[str, builtins.object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> builtins.object: ...
