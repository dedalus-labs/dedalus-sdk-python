# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, TypedDict

from ..._types import SequenceNotStr
from .reasoning import Reasoning
from .tool_choice import ToolChoice

__all__ = ["ModelSettings"]


class ModelSettings(TypedDict, total=False):
    attributes: Dict[str, object]

    audio: Optional["JSONObjectInput"]

    deferred: Optional[bool]

    extra_args: Optional[Dict[str, object]]

    extra_headers: Optional[Dict[str, str]]

    extra_query: Optional[Dict[str, object]]

    frequency_penalty: Optional[float]

    generation_config: Optional["JSONObjectInput"]

    include_usage: Optional[bool]

    input_audio_format: Optional[str]

    input_audio_transcription: Optional["JSONObjectInput"]

    logit_bias: Optional[Dict[str, int]]

    logprobs: Optional[bool]

    max_completion_tokens: Optional[int]

    max_tokens: Optional[int]

    metadata: Optional[Dict[str, str]]

    modalities: Optional[SequenceNotStr[str]]

    n: Optional[int]

    output_audio_format: Optional[str]

    parallel_tool_calls: Optional[bool]

    prediction: Optional["JSONObjectInput"]

    presence_penalty: Optional[float]

    prompt_cache_key: Optional[str]

    reasoning: Optional[Reasoning]
    """**gpt-5 and o-series models only**

    Configuration options for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    """

    reasoning_effort: Optional[str]

    response_format: Optional["JSONObjectInput"]

    safety_identifier: Optional[str]

    safety_settings: Optional[Iterable["JSONObjectInput"]]

    search_parameters: Optional["JSONObjectInput"]

    seed: Optional[int]

    service_tier: Optional[str]

    stop: Union[str, SequenceNotStr[str], None]

    store: Optional[bool]

    stream: Optional[bool]

    stream_options: Optional["JSONObjectInput"]

    structured_output: object

    system_instruction: Optional["JSONObjectInput"]

    temperature: Optional[float]

    thinking: Optional["JSONObjectInput"]

    timeout: Optional[float]

    tool_choice: Optional[ToolChoice]

    tool_config: Optional["JSONObjectInput"]

    top_k: Optional[int]

    top_logprobs: Optional[int]

    top_p: Optional[float]

    truncation: Optional[Literal["auto", "disabled"]]

    turn_detection: Optional["JSONObjectInput"]

    user: Optional[str]

    verbosity: Optional[str]

    voice: Optional[str]

    web_search_options: Optional["JSONObjectInput"]


from .json_object_input import JSONObjectInput
