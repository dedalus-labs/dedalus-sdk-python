from __future__ import annotations

from typing_extensions import TypeAlias

from ....types.chat.parsed_chat_completion import (
    ParsedChoice,
    ParsedChatCompletion,
    ParsedChatCompletionMessage,
)

ParsedChatCompletionSnapshot: TypeAlias = ParsedChatCompletion[object]
ParsedChatCompletionMessageSnapshot: TypeAlias = ParsedChatCompletionMessage[object]
ParsedChoiceSnapshot: TypeAlias = ParsedChoice[object]

__all__ = [
    "ParsedChoiceSnapshot",
    "ParsedChatCompletionMessageSnapshot",
    "ParsedChatCompletionSnapshot",
]
