# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = ["DedalusModel", "Settings", "SettingsReasoning", "SettingsToolChoice", "SettingsToolChoiceMCPToolChoice"]


class SettingsReasoningTyped(TypedDict, total=False):
    effort: Optional[Literal["minimal", "low", "medium", "high"]]

    generate_summary: Optional[Literal["auto", "concise", "detailed"]]

    summary: Optional[Literal["auto", "concise", "detailed"]]


SettingsReasoning: TypeAlias = Union[SettingsReasoningTyped, Dict[str, object]]


class SettingsToolChoiceMCPToolChoice(TypedDict, total=False):
    name: Required[str]

    server_label: Required[str]


SettingsToolChoice: TypeAlias = Union[Literal["auto", "required", "none"], str, SettingsToolChoiceMCPToolChoice]


class Settings(TypedDict, total=False):
    attributes: Dict[str, object]

    audio: Optional[Dict[str, object]]

    disable_automatic_function_calling: bool

    extra_args: Optional[Dict[str, object]]

    extra_headers: Optional[Dict[str, str]]

    extra_query: Optional[Dict[str, object]]

    frequency_penalty: Optional[float]

    generation_config: Optional[Dict[str, object]]

    include_usage: Optional[bool]

    input_audio_format: Optional[str]

    input_audio_transcription: Optional[Dict[str, object]]

    logit_bias: Optional[Dict[str, int]]

    logprobs: Optional[bool]

    max_completion_tokens: Optional[int]

    max_tokens: Optional[int]

    metadata: Optional[Dict[str, str]]

    modalities: Optional[SequenceNotStr[str]]

    n: Optional[int]

    output_audio_format: Optional[str]

    parallel_tool_calls: Optional[bool]

    prediction: Optional[Dict[str, object]]

    presence_penalty: Optional[float]

    prompt_cache_key: Optional[str]

    reasoning: Optional[SettingsReasoning]

    reasoning_effort: Optional[str]

    response_format: Optional[Dict[str, object]]

    response_include: Optional[
        List[
            Literal[
                "code_interpreter_call.outputs",
                "computer_call_output.output.image_url",
                "file_search_call.results",
                "message.input_image.image_url",
                "message.output_text.logprobs",
                "reasoning.encrypted_content",
            ]
        ]
    ]

    safety_identifier: Optional[str]

    safety_settings: Optional[Iterable[Dict[str, object]]]

    seed: Optional[int]

    service_tier: Optional[str]

    stop: Union[str, SequenceNotStr[str], None]

    store: Optional[bool]

    stream: Optional[bool]

    stream_options: Optional[Dict[str, object]]

    structured_output: object

    system_instruction: Optional[Dict[str, object]]

    temperature: Optional[float]

    thinking: Optional[Dict[str, object]]

    timeout: Optional[float]

    tool_choice: Optional[SettingsToolChoice]

    tool_config: Optional[Dict[str, object]]

    top_k: Optional[int]

    top_logprobs: Optional[int]

    top_p: Optional[float]

    truncation: Optional[Literal["auto", "disabled"]]

    turn_detection: Optional[Dict[str, object]]

    use_responses: bool

    user: Optional[str]

    verbosity: Optional[str]

    voice: Optional[str]

    web_search_options: Optional[Dict[str, object]]


class DedalusModel(TypedDict, total=False):
    model: Required[str]
    """
    Model identifier with provider prefix (e.g., 'openai/gpt-5',
    'anthropic/claude-3-5-sonnet').
    """

    settings: Optional[Settings]
    """
    Optional default generation settings (e.g., temperature, max_tokens) applied
    when this model is selected.
    """
