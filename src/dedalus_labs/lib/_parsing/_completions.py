from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, Iterable, cast
from typing_extensions import TypeVar, TypeGuard

import pydantic

from .._tools import PydanticFunctionTool
from ..._types import Omit, omit
from ..._utils import is_dict, is_given
from ..._compat import PYDANTIC_V1, model_parse_json
from ..._models import construct_type_unchecked
from .._pydantic import is_basemodel_type, to_strict_json_schema, is_dataclass_like_type

if TYPE_CHECKING:
    from ...types.chat.completion_create_params import ResponseFormat as ResponseFormatParam
    from ...types.chat.completion import ChoiceMessageToolCallChatCompletionMessageToolCallFunction as Function

ResponseFormatT = TypeVar("ResponseFormatT")


def type_to_response_format_param(
    response_format: type | ResponseFormatParam | Omit,
) -> ResponseFormatParam | Omit:
    """Convert Pydantic model to API response_format parameter."""
    if not is_given(response_format):
        return omit

    if is_dict(response_format):
        return response_format

    response_format = cast(type, response_format)

    if is_basemodel_type(response_format):
        name = response_format.__name__
        json_schema_type = response_format
    elif is_dataclass_like_type(response_format):
        name = response_format.__name__
        json_schema_type = pydantic.TypeAdapter(response_format)
    else:
        raise TypeError(f"Unsupported response_format type - {response_format}")

    return {
        "type": "json_schema",
        "json_schema": {
            "schema": to_strict_json_schema(json_schema_type),
            "name": name,
            "strict": True,
        },
    }


def validate_input_tools(tools: Iterable[Dict[str, Any]] | Omit = omit) -> Iterable[Dict[str, Any]] | Omit:
    """Validate tools for strict parsing support."""
    if not is_given(tools):
        return omit

    for tool in tools:
        if tool.get("type") != "function":
            raise ValueError(f"Only function tools support auto-parsing; got {tool.get('type')}")

        strict = tool.get("function", {}).get("strict")
        if strict is not True:
            name = tool.get("function", {}).get("name", "unknown")
            raise ValueError(f"Tool '{name}' is not strict. Only strict function tools can be auto-parsed")

    return cast(Iterable[Dict[str, Any]], tools)


def parse_chat_completion(
    *,
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
    chat_completion: Any,
    input_tools: Iterable[Dict[str, Any]] | Omit = omit,
) -> Any:
    """Parse completion: response content and tool call arguments into Pydantic models."""
    from ...types.chat.parsed_chat_completion import (
        ParsedChatCompletion,
        ParsedChoice,
        ParsedChatCompletionMessage,
    )
    from ...types.chat.parsed_function_tool_call import ParsedFunctionToolCall, ParsedFunction

    tool_list = list(input_tools) if is_given(input_tools) else []

    choices = []
    for choice in chat_completion.choices:
        message = choice.message

        # Parse tool calls if present
        tool_calls = []
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    parsed_args = _parse_function_tool_arguments(
                        input_tools=tool_list, function=tool_call.function
                    )
                    tool_calls.append(
                        construct_type_unchecked(
                            value={
                                **tool_call.to_dict(),
                                "function": {
                                    **tool_call.function.to_dict(),
                                    "parsed_arguments": parsed_args,
                                },
                            },
                            type_=ParsedFunctionToolCall,
                        )
                    )
                else:
                    tool_calls.append(tool_call)

        # Parse response content
        parsed_content = None
        if is_given(response_format) and not is_dict(response_format):
            if message.content and not getattr(message, "refusal", None):
                parsed_content = _parse_content(response_format, message.content)

        choices.append(
            construct_type_unchecked(
                type_=cast(Any, ParsedChoice),
                value={
                    **choice.to_dict(),
                    "message": {
                        **message.to_dict(),
                        "parsed": parsed_content,
                        "tool_calls": tool_calls if tool_calls else None,
                    },
                },
            )
        )

    return construct_type_unchecked(
        type_=cast(Any, ParsedChatCompletion),
        value={
            **chat_completion.to_dict(),
            "choices": choices,
        },
    )


def _parse_function_tool_arguments(*, input_tools: list[Dict[str, Any]], function: Function) -> object | None:
    """Parse tool call arguments using Pydantic if tool schema is available."""
    input_tool = next(
        (t for t in input_tools if t.get("type") == "function" and t.get("function", {}).get("name") == function.name),
        None,
    )
    if not input_tool:
        return None

    input_fn = input_tool.get("function")
    if isinstance(input_fn, PydanticFunctionTool):
        return model_parse_json(input_fn.model, function.arguments)

    if input_fn and input_fn.get("strict"):
        return json.loads(function.arguments)

    return None


def _parse_content(response_format: type[ResponseFormatT], content: str) -> ResponseFormatT:
    """Deserialize JSON string into typed Pydantic model."""
    if is_basemodel_type(response_format):
        return cast(ResponseFormatT, model_parse_json(response_format, content))

    if is_dataclass_like_type(response_format):
        if PYDANTIC_V1:
            raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {response_format}")
        return pydantic.TypeAdapter(response_format).validate_json(content)

    raise TypeError(f"Unable to automatically parse response format type {response_format}")
