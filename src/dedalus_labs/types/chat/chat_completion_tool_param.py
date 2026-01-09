# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatCompletionToolParam"]


class ChatCompletionToolParam(TypedDict, total=False):
    """A function tool that can be used to generate a response.

    Fields:
    - type (required): Literal["function"]
    - function (required): FunctionObject
    """

    function: Required["FunctionDefinition"]
    """Schema for FunctionObject.

    Fields:

    - description (optional): str
    - name (required): str
    - parameters (optional): FunctionParameters
    - strict (optional): bool | None
    """

    type: Required[Literal["function"]]
    """The type of the tool. Currently, only `function` is supported."""


from ..shared_params.function_definition import FunctionDefinition
