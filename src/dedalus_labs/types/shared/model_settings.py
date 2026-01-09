# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .reasoning import Reasoning
from .tool_choice import ToolChoice

__all__ = ["ModelSettings"]


class ModelSettings(BaseModel):
    attributes: Optional[Dict[str, object]] = None

    audio: Optional["JSONObjectInput"] = None

    deferred: Optional[bool] = None

    extra_args: Optional[Dict[str, object]] = None

    extra_headers: Optional[Dict[str, str]] = None

    extra_query: Optional[Dict[str, object]] = None

    frequency_penalty: Optional[float] = None

    generation_config: Optional["JSONObjectInput"] = None

    include_usage: Optional[bool] = None

    input_audio_format: Optional[str] = None

    input_audio_transcription: Optional["JSONObjectInput"] = None

    logit_bias: Optional[Dict[str, int]] = None

    logprobs: Optional[bool] = None

    max_completion_tokens: Optional[int] = None

    max_tokens: Optional[int] = None

    metadata: Optional[Dict[str, str]] = None

    modalities: Optional[List[str]] = None

    n: Optional[int] = None

    output_audio_format: Optional[str] = None

    parallel_tool_calls: Optional[bool] = None

    prediction: Optional["JSONObjectInput"] = None

    presence_penalty: Optional[float] = None

    prompt_cache_key: Optional[str] = None

    reasoning: Optional[Reasoning] = None
    """**gpt-5 and o-series models only**

    Configuration options for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    """

    reasoning_effort: Optional[str] = None

    response_format: Optional["JSONObjectInput"] = None

    safety_identifier: Optional[str] = None

    safety_settings: Optional[List["JSONObjectInput"]] = None

    search_parameters: Optional["JSONObjectInput"] = None

    seed: Optional[int] = None

    service_tier: Optional[str] = None

    stop: Union[str, List[str], None] = None

    store: Optional[bool] = None

    stream: Optional[bool] = None

    stream_options: Optional["JSONObjectInput"] = None

    structured_output: Optional[object] = None

    system_instruction: Optional["JSONObjectInput"] = None

    temperature: Optional[float] = None

    thinking: Optional["JSONObjectInput"] = None

    timeout: Optional[float] = None

    tool_choice: Optional[ToolChoice] = None

    tool_config: Optional["JSONObjectInput"] = None

    top_k: Optional[int] = None

    top_logprobs: Optional[int] = None

    top_p: Optional[float] = None

    truncation: Optional[Literal["auto", "disabled"]] = None

    turn_detection: Optional["JSONObjectInput"] = None

    user: Optional[str] = None

    verbosity: Optional[str] = None

    voice: Optional[str] = None

    web_search_options: Optional["JSONObjectInput"] = None


from .json_object_input import JSONObjectInput
