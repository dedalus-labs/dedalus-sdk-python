"""Minimal parsing helpers for structured outputs.

Simplified from OpenAI SDK - only core functionality needed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast
from typing_extensions import TypeVar

import pydantic

from ..._types import Omit, omit
from ..._utils import is_dict, is_given
from ..._compat import PYDANTIC_V1, model_parse_json
from .._pydantic import is_basemodel_type, to_strict_json_schema, is_dataclass_like_type

if TYPE_CHECKING:
    from ...types.chat.completion_create_params import ResponseFormat as ResponseFormatParam

ResponseFormatT = TypeVar("ResponseFormatT")


def type_to_response_format_param(
    response_format: type | ResponseFormatParam | Omit,
) -> ResponseFormatParam | Omit:
    """Convert Pydantic model or dict to response_format parameter."""
    if not is_given(response_format):
        return omit

    if is_dict(response_format):
        return response_format

    # Must be a type (Pydantic model or dataclass)
    response_format = cast(type, response_format)

    json_schema_type: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any] | None = None

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


def parse_chat_completion(
    *,
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
    chat_completion: Any,
    input_tools: Any | Omit = omit,
) -> Any:
    """Parse chat completion response into Pydantic model.

    For now, returns the raw completion with a .parsed attribute added.
    Full ParsedChatCompletion type support requires more type infrastructure.
    """
    from ...types.chat.parsed_chat_completion import ParsedChatCompletion

    # Extract and parse the content if response_format was given
    parsed = None
    if is_given(response_format) and not is_dict(response_format):
        message = chat_completion.choices[0].message
        if message.content and not getattr(message, "refusal", None):
            parsed = _parse_content(response_format, message.content)

    # Create a ParsedChatCompletion-like object
    # This is simplified - full implementation would reconstruct all nested types
    class ParsedMessage:
        def __init__(self, original_message, parsed_content):
            self._original = original_message
            self.parsed = parsed_content
            self.content = original_message.content
            self.role = original_message.role
            self.refusal = getattr(original_message, "refusal", None)

    class ParsedChoice:
        def __init__(self, original_choice, parsed_message):
            self.message = parsed_message
            self.finish_reason = original_choice.finish_reason
            self.index = original_choice.index

    # Build parsed completion
    parsed_message = ParsedMessage(chat_completion.choices[0].message, parsed)
    parsed_choice = ParsedChoice(chat_completion.choices[0], parsed_message)

    # Return object with same interface as original but with parsed message
    result = chat_completion
    result.choices = [parsed_choice]
    return result


def _parse_content(response_format: type[ResponseFormatT], content: str) -> ResponseFormatT:
    """Parse JSON content into Pydantic model."""
    if is_basemodel_type(response_format):
        return cast(ResponseFormatT, model_parse_json(response_format, content))

    if is_dataclass_like_type(response_format):
        if PYDANTIC_V1:
            raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {response_format}")
        return pydantic.TypeAdapter(response_format).validate_json(content)

    raise TypeError(f"Unable to automatically parse response format type {response_format}")


def validate_input_tools(tools: Any | Omit = omit) -> Any | Omit:
    """Validate input tools (simplified - just pass through for now)."""
    return tools
