# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .function import Function
from ..._models import BaseModel

__all__ = ["ChoiceDeltaToolCall"]


class ChoiceDeltaToolCall(BaseModel):
    index: int

    id: Optional[str] = None
    """The ID of the tool call."""

    function: Optional[Function] = None
    """The function that the model called.

    Fields:

    - name (required): str
    - arguments (required): str
    """

    type: Optional[Literal["function"]] = None
    """The type of the tool. Currently, only `function` is supported."""
