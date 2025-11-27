# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..chat.reasoning import Reasoning
from ..chat.tool_choice import ToolChoice

__all__ = ["DedalusModel", "Settings"]


class Settings(BaseModel):
    attributes: Optional[Dict[str, object]] = None

    audio: Optional[Dict[str, object]] = None

    deferred: Optional[bool] = None

    extra_args: Optional[Dict[str, object]] = None

    extra_headers: Optional[Dict[str, str]] = None

    extra_query: Optional[Dict[str, object]] = None

    frequency_penalty: Optional[float] = None

    generation_config: Optional[Dict[str, object]] = None

    include_usage: Optional[bool] = None

    input_audio_format: Optional[str] = None

    input_audio_transcription: Optional[Dict[str, object]] = None

    logit_bias: Optional[Dict[str, int]] = None

    logprobs: Optional[bool] = None

    max_completion_tokens: Optional[int] = None

    max_tokens: Optional[int] = None

    metadata: Optional[Dict[str, str]] = None

    modalities: Optional[List[str]] = None

    n: Optional[int] = None

    output_audio_format: Optional[str] = None

    parallel_tool_calls: Optional[bool] = None

    prediction: Optional[Dict[str, object]] = None

    presence_penalty: Optional[float] = None

    prompt_cache_key: Optional[str] = None

    reasoning: Optional[Reasoning] = None

    reasoning_effort: Optional[str] = None

    response_format: Optional[Dict[str, object]] = None

    safety_identifier: Optional[str] = None

    safety_settings: Optional[List[Dict[str, object]]] = None

    search_parameters: Optional[Dict[str, object]] = None

    seed: Optional[int] = None

    service_tier: Optional[str] = None

    stop: Union[str, List[str], None] = None

    store: Optional[bool] = None

    stream: Optional[bool] = None

    stream_options: Optional[Dict[str, object]] = None

    structured_output: Optional[object] = None

    system_instruction: Optional[Dict[str, object]] = None

    temperature: Optional[float] = None

    thinking: Optional[Dict[str, object]] = None

    timeout: Optional[float] = None

    tool_choice: Optional[ToolChoice] = None

    tool_config: Optional[Dict[str, object]] = None

    top_k: Optional[int] = None

    top_logprobs: Optional[int] = None

    top_p: Optional[float] = None

    truncation: Optional[Literal["auto", "disabled"]] = None

    turn_detection: Optional[Dict[str, object]] = None

    user: Optional[str] = None

    verbosity: Optional[str] = None

    voice: Optional[str] = None

    web_search_options: Optional[Dict[str, object]] = None


class DedalusModel(BaseModel):
    model: str
    """
    Model identifier with provider prefix (e.g., 'openai/gpt-5',
    'anthropic/claude-3-5-sonnet').
    """

    settings: Optional[Settings] = None
    """
    Optional default generation settings (e.g., temperature, max_tokens) applied
    when this model is selected.
    """
