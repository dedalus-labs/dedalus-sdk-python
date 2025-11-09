# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["DedalusModel", "Settings", "SettingsReasoning", "SettingsToolChoice", "SettingsToolChoiceMCPToolChoice"]


class SettingsReasoning(BaseModel):
    effort: Optional[Literal["minimal", "low", "medium", "high"]] = None

    generate_summary: Optional[Literal["auto", "concise", "detailed"]] = None

    summary: Optional[Literal["auto", "concise", "detailed"]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class SettingsToolChoiceMCPToolChoice(BaseModel):
    name: str

    server_label: str


SettingsToolChoice: TypeAlias = Union[
    Literal["auto", "required", "none"], str, Dict[str, object], SettingsToolChoiceMCPToolChoice, None
]


class Settings(BaseModel):
    attributes: Optional[Dict[str, object]] = None

    audio: Optional[Dict[str, object]] = None

    deferred: Optional[bool] = None

    disable_automatic_function_calling: Optional[bool] = None

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

    reasoning: Optional[SettingsReasoning] = None

    reasoning_effort: Optional[str] = None

    response_format: Optional[Dict[str, object]] = None

    response_include: Optional[
        List[
            Literal[
                "file_search_call.results",
                "web_search_call.results",
                "web_search_call.action.sources",
                "message.input_image.image_url",
                "computer_call_output.output.image_url",
                "code_interpreter_call.outputs",
                "reasoning.encrypted_content",
                "message.output_text.logprobs",
            ]
        ]
    ] = None

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

    tool_choice: Optional[SettingsToolChoice] = None

    tool_config: Optional[Dict[str, object]] = None

    top_k: Optional[int] = None

    top_logprobs: Optional[int] = None

    top_p: Optional[float] = None

    truncation: Optional[Literal["auto", "disabled"]] = None

    turn_detection: Optional[Dict[str, object]] = None

    use_responses: Optional[bool] = None

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
