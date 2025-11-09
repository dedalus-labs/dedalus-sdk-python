# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .completion import ChoiceMessageToolCallChatCompletionMessageToolCallFunction as Function
from .completion import ChoiceMessageToolCallChatCompletionMessageToolCall as FunctionToolCall

__all__ = ["ParsedFunctionToolCall", "ParsedFunction"]

# pyright: reportIncompatibleVariableOverride=false


class ParsedFunction(Function):
    parsed_arguments: Optional[object] = None
    """Parsed tool call arguments as Pydantic model instance or dict."""


class ParsedFunctionToolCall(FunctionToolCall):
    function: ParsedFunction
    """The function that the model called."""
