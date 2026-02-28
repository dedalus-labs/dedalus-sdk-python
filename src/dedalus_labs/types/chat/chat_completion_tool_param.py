# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..shared_params.function_definition import FunctionDefinition

__all__ = ["ChatCompletionToolParam"]


class ChatCompletionToolParam(TypedDict, total=False):
    """Schema for Tool.

    Fields:
    - type (optional): ToolTypes
    - function (required): Function
    """

    function: Required[FunctionDefinition]
    """Schema for Function.

    Fields:

    - name (required): str
    """

    type: Literal["function"]
