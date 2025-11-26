# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .choice_delta_tool_call import ChoiceDeltaToolCall
from .choice_delta_function_call import ChoiceDeltaFunctionCall

__all__ = ["ChoiceDelta"]


class ChoiceDelta(BaseModel):
    content: Optional[str] = None

    function_call: Optional[ChoiceDeltaFunctionCall] = None

    refusal: Optional[str] = None

    role: Optional[Literal["developer", "system", "user", "assistant", "tool"]] = None

    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
