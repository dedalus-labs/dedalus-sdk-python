# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "StreamChunk",
    "Choice",
    "ChoiceDelta",
    "ChoiceDeltaFunctionCall",
    "ChoiceDeltaToolCall",
    "ChoiceDeltaToolCallFunction",
    "ChoiceLogprobs",
    "ChoiceLogprobsContent",
    "ChoiceLogprobsContentTopLogprob",
    "ChoiceLogprobsRefusal",
    "ChoiceLogprobsRefusalTopLogprob",
    "Usage",
    "UsageCompletionTokensDetails",
    "UsagePromptTokensDetails",
]


class ChoiceDeltaFunctionCall(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None


class ChoiceDeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None

    name: Optional[str] = None


class ChoiceDeltaToolCall(BaseModel):
    index: int

    id: Optional[str] = None

    function: Optional[ChoiceDeltaToolCallFunction] = None

    type: Optional[Literal["function"]] = None


class ChoiceDelta(BaseModel):
    content: Optional[str] = None

    function_call: Optional[ChoiceDeltaFunctionCall] = None

    refusal: Optional[str] = None

    role: Optional[Literal["developer", "system", "user", "assistant", "tool"]] = None

    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None


class ChoiceLogprobsContentTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None


class ChoiceLogprobsContent(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[ChoiceLogprobsContentTopLogprob]

    bytes: Optional[List[int]] = None


class ChoiceLogprobsRefusalTopLogprob(BaseModel):
    token: str

    logprob: float

    bytes: Optional[List[int]] = None


class ChoiceLogprobsRefusal(BaseModel):
    token: str

    logprob: float

    top_logprobs: List[ChoiceLogprobsRefusalTopLogprob]

    bytes: Optional[List[int]] = None


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChoiceLogprobsContent]] = None

    refusal: Optional[List[ChoiceLogprobsRefusal]] = None


class Choice(BaseModel):
    delta: ChoiceDelta

    index: int

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None

    logprobs: Optional[ChoiceLogprobs] = None


class UsageCompletionTokensDetails(BaseModel):
    accepted_prediction_tokens: Optional[int] = None

    audio_tokens: Optional[int] = None

    reasoning_tokens: Optional[int] = None

    rejected_prediction_tokens: Optional[int] = None


class UsagePromptTokensDetails(BaseModel):
    audio_tokens: Optional[int] = None

    cached_tokens: Optional[int] = None


class Usage(BaseModel):
    completion_tokens: int

    prompt_tokens: int

    total_tokens: int

    completion_tokens_details: Optional[UsageCompletionTokensDetails] = None

    prompt_tokens_details: Optional[UsagePromptTokensDetails] = None


class StreamChunk(BaseModel):
    id: str

    choices: List[Choice]

    created: int

    model: str

    object: Literal["chat.completion.chunk"]

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    system_fingerprint: Optional[str] = None

    usage: Optional[Usage] = None
