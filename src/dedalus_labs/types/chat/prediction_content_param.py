# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .chat_completion_content_part_text_param import ChatCompletionContentPartTextParam

__all__ = ["PredictionContentParam"]


class PredictionContentParam(TypedDict, total=False):
    """
    Static predicted output content, such as the content of a text file that is
    being regenerated.

    Fields:
    - type (required): Literal["content"]
    - content (required): str | Annotated[list[ChatCompletionRequestMessageContentPartText], MinLen(1), ArrayTitle("PredictionContentArray")]
    """

    content: Required[Union[str, Iterable[ChatCompletionContentPartTextParam]]]
    """
    The content that should be matched when generating a model response. If
    generated tokens would match this content, the entire model response can be
    returned much more quickly.
    """

    type: Required[Literal["content"]]
    """The type of the predicted content you want to provide.

    This type is currently always `content`.
    """
