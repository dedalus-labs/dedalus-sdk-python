# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .chat_completion_content_part_file_param import ChatCompletionContentPartFileParam
from .chat_completion_content_part_text_param import ChatCompletionContentPartTextParam
from .chat_completion_content_part_image_param import ChatCompletionContentPartImageParam
from .chat_completion_content_part_input_audio_param import ChatCompletionContentPartInputAudioParam

__all__ = ["ChatCompletionUserMessageParam", "ContentChatCompletionRequestUserMessageContentArray"]

ContentChatCompletionRequestUserMessageContentArray: TypeAlias = Union[
    ChatCompletionContentPartTextParam,
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartInputAudioParam,
    ChatCompletionContentPartFileParam,
]


class ChatCompletionUserMessageParam(TypedDict, total=False):
    """
    Messages sent by an end user, containing prompts or additional context
    information.

    Fields:
    - content (required): str | Annotated[list[ChatCompletionRequestUserMessageContentPart], MinLen(1), ArrayTitle("ChatCompletionRequestUserMessageContentArray")]
    - role (required): Literal["user"]
    - name (optional): str
    """

    content: Required[Union[str, Iterable[ContentChatCompletionRequestUserMessageContentArray]]]
    """The contents of the user message."""

    role: Required[Literal["user"]]
    """The role of the messages author, in this case `user`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """
