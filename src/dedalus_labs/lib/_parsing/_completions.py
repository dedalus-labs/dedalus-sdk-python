from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, Iterable, cast
from typing_extensions import TypeGuard, TypeVar

import pydantic

from .._tools import PydanticFunctionTool
from ..._types import Omit, omit
from ..._utils import is_dict, is_given
from ..._compat import PYDANTIC_V1, model_parse_json
from ..._models import construct_type_unchecked
from .._pydantic import is_basemodel_type, is_dataclass_like_type, to_strict_json_schema

if TYPE_CHECKING:
    # Import proper ResponseFormat type from server schemas
    # At runtime this is just a dict, but for type checking we want the union
    ResponseFormatParam = Dict[str, Any]
else:
    ResponseFormatParam = Dict[str, Any]

if TYPE_CHECKING:
    from ...types.chat.completion import (
        Completion,
        Choice,
        ChoiceMessage,
        ChoiceMessageToolCallChatCompletionMessageToolCallFunction as Function,
    )
    from ...types.chat.parsed_chat_completion import (
        ParsedChoice,
        ParsedChatCompletion,
        ParsedChatCompletionMessage,
    )
    from ...types.chat.parsed_function_tool_call import ParsedFunctionToolCall


ResponseFormatT = TypeVar(
    "ResponseFormatT",
    default=None,
)
_default_response_format: None = None


def type_to_response_format_param(
    response_format: type | ResponseFormatParam | Omit,
) -> ResponseFormatParam | Omit:
    """Convert a response_format convenience value into the wire schema."""
    if not is_given(response_format):
        return omit

    if is_dict(response_format):
        return cast(ResponseFormatParam, response_format)

    response_format = cast(type, response_format)

    if is_basemodel_type(response_format):
        name = response_format.__name__
        json_schema_type = response_format
    elif is_dataclass_like_type(response_format):
        name = response_format.__name__
        json_schema_type = pydantic.TypeAdapter(response_format)
    else:
        raise TypeError(f"Unsupported response_format type: {response_format}")

    return {
        "type": "json_schema",
        "json_schema": {
            "schema": to_strict_json_schema(json_schema_type),
            "name": name,
            "strict": True,
        },
    }


def validate_input_tools(tools: Iterable[Dict[str, Any]] | Omit = omit) -> Iterable[Dict[str, Any]] | Omit:
    """Ensure all provided tools can participate in automatic parsing."""
    if not is_given(tools):
        return omit

    for tool in tools:
        if tool.get("type") != "function":
            raise ValueError(f"Only function tools support auto-parsing; received '{tool.get('type')}'.")

        strict = tool.get("function", {}).get("strict")
        if strict is not True:
            name = tool.get("function", {}).get("name", "unknown_function")
            raise ValueError(f"Tool '{name}' is not strict. Only strict function tools can be auto-parsed.")

    return cast(Iterable[Dict[str, Any]], tools)


def parse_chat_completion(
    *,
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
    chat_completion: Completion | ParsedChatCompletion[object],
    input_tools: Iterable[Dict[str, Any]] | Omit = omit,
) -> ParsedChatCompletion[ResponseFormatT]:
    """Parse a completion's content & tool calls into structured objects."""
    from ...types.chat.parsed_chat_completion import (
        ParsedChoice,
        ParsedChatCompletion,
    )
    from ...types.chat.parsed_function_tool_call import ParsedFunctionToolCall

    tool_list = list(input_tools) if is_given(input_tools) else []

    parsed_choices = []
    for choice in chat_completion.choices:
        message = choice.message

        tool_calls = []
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:  # type: ignore[attr-defined]
                if getattr(tool_call, "type", None) == "function":
                    parsed_args = parse_function_tool_arguments(
                        input_tools=tool_list,
                        function=tool_call.function,  # type: ignore[attr-defined]
                    )
                    tool_calls.append(
                        construct_type_unchecked(
                            value={
                                **tool_call.to_dict(),
                                "function": {
                                    **tool_call.function.to_dict(),  # type: ignore[attr-defined]
                                    "parsed_arguments": parsed_args,
                                },
                            },
                            type_=ParsedFunctionToolCall,
                        )
                    )
                else:
                    tool_calls.append(tool_call)

        parsed_choices.append(
            construct_type_unchecked(
                type_=cast(Any, ParsedChoice)[solve_response_format_t(response_format)],
                value={
                    **choice.to_dict(),
                    "message": {
                        **message.to_dict(),
                        "parsed": maybe_parse_content(response_format=response_format, message=message),
                        "tool_calls": tool_calls if tool_calls else None,
                    },
                },
            )
        )

    return cast(
        ParsedChatCompletion[ResponseFormatT],
        construct_type_unchecked(
            type_=cast(Any, ParsedChatCompletion)[solve_response_format_t(response_format)],
            value={
                **chat_completion.to_dict(),
                "choices": parsed_choices,
            },
        ),
    )


def maybe_parse_content(
    *,
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
    message: ChoiceMessage | ParsedChatCompletionMessage[object],
) -> ResponseFormatT | None:
    if has_rich_response_format(response_format) and getattr(message, "content", None) and not getattr(
        message, "refusal", None
    ):
        return _parse_content(response_format, cast(str, message.content))

    return None


def has_parseable_input(
    *,
    response_format: type | ResponseFormatParam | Omit,
    input_tools: Iterable[Dict[str, Any]] | Omit = omit,
) -> bool:
    if has_rich_response_format(response_format):
        return True

    for input_tool in input_tools or []:
        if is_parseable_tool(input_tool):
            return True

    return False


def solve_response_format_t(
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
) -> type[ResponseFormatT]:
    if has_rich_response_format(response_format):
        return cast("type[ResponseFormatT]", response_format)

    return cast("type[ResponseFormatT]", _default_response_format)


def get_input_tool_by_name(
    *,
    input_tools: list[Dict[str, Any]],
    name: str,
) -> Dict[str, Any] | None:
    return next(
        (tool for tool in input_tools if tool.get("type") == "function" and tool.get("function", {}).get("name") == name),
        None,
    )


def parse_function_tool_arguments(
    *,
    input_tools: list[Dict[str, Any]],
    function: "Function",
) -> object | None:
    input_tool = get_input_tool_by_name(input_tools=input_tools, name=function.name)
    if not input_tool:
        return None

    definition = input_tool.get("function")
    if isinstance(definition, PydanticFunctionTool):
        return model_parse_json(definition.model, function.arguments)

    if isinstance(definition, dict) and definition.get("strict") and definition.get("parameters"):
        return json.loads(function.arguments)

    return None


def has_rich_response_format(
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
) -> TypeGuard[type[ResponseFormatT]]:
    return is_given(response_format) and not is_response_format_param(response_format)


def is_response_format_param(response_format: object) -> TypeGuard[ResponseFormatParam]:
    return is_dict(response_format)


def is_parseable_tool(tool: Dict[str, Any]) -> bool:
    if tool.get("type") != "function":
        return False

    definition = tool.get("function")
    if isinstance(definition, PydanticFunctionTool):
        return True

    return bool(isinstance(definition, dict) and definition.get("strict"))


def _parse_content(response_format: type[ResponseFormatT], content: str) -> ResponseFormatT:
    if is_basemodel_type(response_format):
        return cast(ResponseFormatT, model_parse_json(response_format, content))

    if is_dataclass_like_type(response_format):
        if PYDANTIC_V1:
            raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {response_format}")
        return pydantic.TypeAdapter(response_format).validate_json(content)

    raise TypeError(f"Unable to automatically parse response format type {response_format}")


__all__ = [
    "ResponseFormatT",
    "get_input_tool_by_name",
    "has_parseable_input",
    "maybe_parse_content",
    "parse_chat_completion",
    "parse_function_tool_arguments",
    "solve_response_format_t",
    "type_to_response_format_param",
    "validate_input_tools",
]
