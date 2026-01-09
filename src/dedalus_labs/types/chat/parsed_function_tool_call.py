# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .chat_completion_message_tool_call import ChatCompletionMessageToolCall as FunctionToolCall, Function

__all__ = ["ParsedFunctionToolCall", "ParsedFunction"]

# pyright: reportIncompatibleVariableOverride=false


class ParsedFunction(Function):
    parsed_arguments: Optional[object] = None
    """Parsed tool call arguments as Pydantic model instance or dict."""


class ParsedFunctionToolCall(FunctionToolCall):
    function: ParsedFunction
    """The function that the model called."""
