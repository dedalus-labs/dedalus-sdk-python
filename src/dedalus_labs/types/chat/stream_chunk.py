# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .chat_completion_token_logprob import ChatCompletionTokenLogprob

__all__ = [
    "StreamChunk",
    "Choice",
    "ChoiceDelta",
    "ChoiceDeltaFunctionCall",
    "ChoiceDeltaToolCall",
    "ChoiceDeltaToolCallFunction",
    "ChoiceLogprobs",
    "Usage",
    "UsageCompletionTokensDetails",
    "UsagePromptTokensDetails",
]


class ChoiceDeltaFunctionCall(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChoiceDeltaToolCall(BaseModel):
    index: int

    id: Optional[str] = None

    function: Optional[ChoiceDeltaToolCallFunction] = None

    type: Optional[Literal["function"]] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChoiceDelta(BaseModel):
    content: Optional[str] = None

    function_call: Optional[ChoiceDeltaFunctionCall] = None

    refusal: Optional[str] = None

    role: Optional[Literal["developer", "system", "user", "assistant", "tool"]] = None

    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChatCompletionTokenLogprob]] = None
    """Log probabilities for the content tokens"""

    refusal: Optional[List[ChatCompletionTokenLogprob]] = None
    """Log probabilities for refusal tokens, if any"""


class Choice(BaseModel):
    delta: ChoiceDelta
    """Delta content for streaming responses"""

    index: int
    """The index of this choice in the list of choices"""

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
    """The reason the model stopped (only in final chunk)"""

    logprobs: Optional[ChoiceLogprobs] = None
    """Log probability information for the choice."""


class UsageCompletionTokensDetails(BaseModel):
    accepted_prediction_tokens: Optional[int] = None

    audio_tokens: Optional[int] = None

    reasoning_tokens: Optional[int] = None

    rejected_prediction_tokens: Optional[int] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class UsagePromptTokensDetails(BaseModel):
    audio_tokens: Optional[int] = None

    cached_tokens: Optional[int] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class Usage(BaseModel):
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int

    completion_tokens_details: Optional[UsageCompletionTokensDetails] = None

    prompt_tokens_details: Optional[UsagePromptTokensDetails] = None

    __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]
    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class StreamChunk(BaseModel):
    id: str
    """Unique identifier for the chat completion"""

    choices: List[Choice]
    """List of completion choice chunks"""

    created: int
    """Unix timestamp when the chunk was created"""

    model: str
    """ID of the model used for the completion"""

    object: Optional[Literal["chat.completion.chunk"]] = None
    """Object type, always 'chat.completion.chunk'"""

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None
    """Service tier used for processing the request"""

    system_fingerprint: Optional[str] = None
    """System fingerprint representing backend configuration"""

    usage: Optional[Usage] = None
    """Usage statistics (only in final chunk with stream_options.include_usage=true)"""
