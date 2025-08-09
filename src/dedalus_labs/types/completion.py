# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Completion",
    "Choice",
    "ChoiceMessage",
    "ChoiceMessageAnnotation",
    "ChoiceMessageAnnotationURLCitation",
    "ChoiceMessageAudio",
    "ChoiceMessageFunctionCall",
    "ChoiceMessageToolCall",
    "ChoiceMessageToolCallFunction",
    "ChoiceLogprobs",
    "ChoiceLogprobsContent",
    "ChoiceLogprobsContentTopLogprob",
    "ChoiceLogprobsRefusal",
    "ChoiceLogprobsRefusalTopLogprob",
    "Usage",
    "UsageCompletionTokensDetails",
    "UsagePromptTokensDetails",
]


class ChoiceMessageAnnotationURLCitation(BaseModel):
    end_index: int

    start_index: int

    title: str

    url: str


class ChoiceMessageAnnotation(BaseModel):
    type: Literal["url_citation"]

    url_citation: ChoiceMessageAnnotationURLCitation


class ChoiceMessageAudio(BaseModel):
    id: str

    data: str

    expires_at: int

    transcript: str


class ChoiceMessageFunctionCall(BaseModel):
    arguments: str

    name: str


class ChoiceMessageToolCallFunction(BaseModel):
    arguments: str

    name: str


class ChoiceMessageToolCall(BaseModel):
    id: str

    function: ChoiceMessageToolCallFunction

    type: Literal["function"]


class ChoiceMessage(BaseModel):
    role: Literal["assistant"]

    annotations: Optional[List[ChoiceMessageAnnotation]] = None

    audio: Optional[ChoiceMessageAudio] = None

    content: Optional[str] = None

    function_call: Optional[ChoiceMessageFunctionCall] = None

    refusal: Optional[str] = None

    tool_calls: Optional[List[ChoiceMessageToolCall]] = None


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
    finish_reason: Literal["stop", "length", "tool_calls", "content_filter", "function_call"]

    index: int

    message: ChoiceMessage

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


class Completion(BaseModel):
    id: str

    choices: List[Choice]

    created: int

    model: str

    object: Literal["chat.completion"]

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None

    system_fingerprint: Optional[str] = None

    usage: Optional[Usage] = None
