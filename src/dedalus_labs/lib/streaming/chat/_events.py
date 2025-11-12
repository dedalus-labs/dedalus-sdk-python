from __future__ import annotations

from typing import Generic, List, Optional, Union
from typing_extensions import Literal

from ._types import ParsedChatCompletionSnapshot
from ...._models import BaseModel, GenericModel
from ..._parsing import ResponseFormatT
from ....types.chat.stream_chunk import StreamChunk
from ....types.chat.chat_completion_token_logprob import ChatCompletionTokenLogprob


class ChunkEvent(BaseModel):
    type: Literal["chunk"]
    chunk: StreamChunk
    snapshot: ParsedChatCompletionSnapshot


class ContentDeltaEvent(BaseModel):
    type: Literal["content.delta"]
    delta: str
    snapshot: str
    parsed: Optional[object] = None


class ContentDoneEvent(GenericModel, Generic[ResponseFormatT]):
    type: Literal["content.done"]
    content: str
    parsed: Optional[ResponseFormatT] = None


class RefusalDeltaEvent(BaseModel):
    type: Literal["refusal.delta"]
    delta: str
    snapshot: str


class RefusalDoneEvent(BaseModel):
    type: Literal["refusal.done"]
    refusal: str


class FunctionToolCallArgumentsDeltaEvent(BaseModel):
    type: Literal["tool_calls.function.arguments.delta"]
    name: str
    index: int
    arguments: str
    parsed_arguments: object
    arguments_delta: str


class FunctionToolCallArgumentsDoneEvent(BaseModel):
    type: Literal["tool_calls.function.arguments.done"]
    name: str
    index: int
    arguments: str
    parsed_arguments: object


class LogprobsContentDeltaEvent(BaseModel):
    type: Literal["logprobs.content.delta"]
    content: List[ChatCompletionTokenLogprob]
    snapshot: List[ChatCompletionTokenLogprob]


class LogprobsContentDoneEvent(BaseModel):
    type: Literal["logprobs.content.done"]
    content: List[ChatCompletionTokenLogprob]


class LogprobsRefusalDeltaEvent(BaseModel):
    type: Literal["logprobs.refusal.delta"]
    refusal: List[ChatCompletionTokenLogprob]
    snapshot: List[ChatCompletionTokenLogprob]


class LogprobsRefusalDoneEvent(BaseModel):
    type: Literal["logprobs.refusal.done"]
    refusal: List[ChatCompletionTokenLogprob]


ChatCompletionStreamEvent = Union[
    ChunkEvent,
    ContentDeltaEvent,
    ContentDoneEvent[ResponseFormatT],
    RefusalDeltaEvent,
    RefusalDoneEvent,
    FunctionToolCallArgumentsDeltaEvent,
    FunctionToolCallArgumentsDoneEvent,
    LogprobsContentDeltaEvent,
    LogprobsContentDoneEvent,
    LogprobsRefusalDeltaEvent,
    LogprobsRefusalDoneEvent,
]


__all__ = [
    "ChatCompletionStreamEvent",
    "ChunkEvent",
    "ContentDeltaEvent",
    "ContentDoneEvent",
    "FunctionToolCallArgumentsDeltaEvent",
    "FunctionToolCallArgumentsDoneEvent",
    "LogprobsContentDeltaEvent",
    "LogprobsContentDoneEvent",
    "LogprobsRefusalDeltaEvent",
    "LogprobsRefusalDoneEvent",
    "RefusalDeltaEvent",
    "RefusalDoneEvent",
]
