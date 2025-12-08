# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .function import Function
from ..._models import BaseModel

__all__ = ["ChatCompletionMessageToolCall"]


class ChatCompletionMessageToolCall(BaseModel):
    """A call to a function tool created by the model.

    Fields:
    - id (required): str
    - type (required): Literal["function"]
    - function (required): Function
    - thought_signature (optional): str
    """

    id: str
    """The ID of the tool call."""

    function: Function
    """The function that the model called."""

    type: Literal["function"]
    """The type of the tool. Currently, only `function` is supported."""

    thought_signature: Optional[str] = None
    """
    Opaque signature for thought continuity in multi-turn tool use (Google-specific,
    base64 encoded)
    """
