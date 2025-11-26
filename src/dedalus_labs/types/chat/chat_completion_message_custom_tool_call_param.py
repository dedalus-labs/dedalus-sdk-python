# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .custom_param import CustomParam

__all__ = ["ChatCompletionMessageCustomToolCallParam"]


class ChatCompletionMessageCustomToolCallParam(TypedDict, total=False):
    id: Required[str]
    """The ID of the tool call."""

    custom: Required[CustomParam]
    """The custom tool that the model called."""

    type: Required[Literal["custom"]]
    """The type of the tool. Always `custom`."""
