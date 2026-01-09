# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .chat_completion_content_part_text_param import ChatCompletionContentPartTextParam

__all__ = ["ChatCompletionToolMessageParam"]


class ChatCompletionToolMessageParam(TypedDict, total=False):
    """Schema for ChatCompletionRequestToolMessage.

    Fields:
    - role (required): Literal["tool"]
    - content (required): str | Annotated[list[ChatCompletionRequestToolMessageContentPart], MinLen(1), ArrayTitle("ChatCompletionRequestToolMessageContentArray")]
    - tool_call_id (required): str
    """

    content: Required[Union[str, Iterable[ChatCompletionContentPartTextParam]]]
    """The contents of the tool message."""

    role: Required[Literal["tool"]]
    """The role of the messages author, in this case `tool`."""

    tool_call_id: Required[str]
    """Tool call that this message is responding to."""
