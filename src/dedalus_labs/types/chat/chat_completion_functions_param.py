# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ChatCompletionFunctionsParam"]


class ChatCompletionFunctionsParam(TypedDict, total=False):
    """Schema for ChatCompletionFunctions.

    Fields:
    - description (optional): str
    - name (required): str
    - parameters (optional): FunctionParameters
    """

    name: Required[str]
    """The name of the function to be called.

    Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length
    of 64.
    """

    description: str
    """
    A description of what the function does, used by the model to choose when and
    how to call the function.
    """

    parameters: "JSONObjectInput"
    """The parameters the functions accepts, described as a JSON Schema object.

    See the [guide](https://platform.openai.com/docs/guides/function-calling) for
    examples, and the
    [JSON Schema reference](https://json-schema.org/understanding-json-schema/) for
    documentation about the format.

    Omitting `parameters` defines a function with an empty parameter list.
    """


from ..shared_params.json_object_input import JSONObjectInput
