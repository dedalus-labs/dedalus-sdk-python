# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .function import Function
from ..._models import BaseModel

__all__ = ["ChatCompletionMessageToolCall"]


class ChatCompletionMessageToolCall(BaseModel):
    id: str
    """The ID of the tool call."""

    function: Function
    """The function that the model called."""

    type: Literal["function"]
    """The type of the tool. Currently, only `function` is supported."""
