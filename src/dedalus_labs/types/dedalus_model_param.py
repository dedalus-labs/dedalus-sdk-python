# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["DedalusModelParam"]


class DedalusModelParam(TypedDict, total=False):
    name: Required[str]
    """Model name (e.g., 'gpt-4', 'claude-3-5-sonnet')"""

    attributes: Optional[Dict[str, float]]
    """
    [Dedalus] Custom attributes for intelligent model routing (e.g., intelligence,
    speed, creativity, cost).
    """

    frequency_penalty: Optional[float]
    """Penalize new tokens based on their frequency in the text so far."""

    logit_bias: Optional[Dict[str, float]]
    """Modify the likelihood of specified tokens appearing."""

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens."""

    max_completion_tokens: Optional[int]
    """An upper bound for the number of tokens that can be generated for a completion."""

    max_tokens: Optional[int]
    """Maximum number of tokens to generate."""

    metadata: Optional[Dict[str, str]]
    """[Dedalus] Additional metadata for request tracking and debugging."""

    n: Optional[int]
    """Number of completions to generate for each prompt."""

    parallel_tool_calls: Optional[bool]
    """Whether to enable parallel function calling."""

    presence_penalty: Optional[float]
    """Penalize new tokens based on whether they appear in the text so far."""

    response_format: Optional[Dict[str, object]]
    """Format for the model output (e.g., {'type': 'json_object'})."""

    seed: Optional[int]
    """Seed for deterministic sampling."""

    service_tier: Optional[str]
    """Latency tier for the request (e.g., 'auto', 'default')."""

    stop: Union[str, SequenceNotStr[str], None]
    """Up to 4 sequences where the API will stop generating further tokens."""

    stream: Optional[bool]
    """Whether to stream back partial progress."""

    stream_options: Optional[Dict[str, object]]
    """Options for streaming responses."""

    temperature: Optional[float]
    """Sampling temperature (0 to 2). Higher values make output more random."""

    tool_choice: Union[str, Dict[str, object], None]
    """Controls which tool is called by the model."""

    tools: Optional[Iterable[Dict[str, object]]]
    """List of tools the model may call."""

    top_logprobs: Optional[int]
    """Number of most likely tokens to return at each token position."""

    top_p: Optional[float]
    """Nucleus sampling parameter. Alternative to temperature."""

    user: Optional[str]
    """A unique identifier representing your end-user."""
