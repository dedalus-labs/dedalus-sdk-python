# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .custom import Custom
from ..._models import BaseModel

__all__ = ["ChatCompletionMessageCustomToolCall"]


class ChatCompletionMessageCustomToolCall(BaseModel):
    id: str
    """The ID of the tool call."""

    custom: Custom
    """The custom tool that the model called."""

    type: Literal["custom"]
    """The type of the tool. Always `custom`."""
