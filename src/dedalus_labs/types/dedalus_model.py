# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, List, Union, Optional

from .._models import BaseModel

__all__ = ["DedalusModel"]


class DedalusModel(BaseModel):
    id: str
    """Model identifier"""

    attributes: Optional[Dict[str, float]] = None
    """
    [Dedalus] Custom attributes for intelligent model routing (e.g., intelligence,
    speed, creativity, cost).
    """

    created: Optional[int] = None
    """Unix timestamp of model creation"""

    frequency_penalty: Optional[float] = None
    """Penalize new tokens based on their frequency in the text so far."""

    logit_bias: Optional[Dict[str, float]] = None
    """Modify the likelihood of specified tokens appearing."""

    logprobs: Optional[bool] = None
    """Whether to return log probabilities of the output tokens."""

    max_completion_tokens: Optional[int] = None
    """An upper bound for the number of tokens that can be generated for a completion."""

    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    metadata: Optional[Dict[str, str]] = None
    """[Dedalus] Additional metadata for request tracking and debugging."""

    n: Optional[int] = None
    """Number of completions to generate for each prompt."""

    name: Optional[str] = None
    """Model name (alias for id)"""

    object: Optional[str] = None
    """Object type, always 'model'"""

    owned_by: Optional[str] = None
    """Organization that owns this model"""

    parallel_tool_calls: Optional[bool] = None
    """Whether to enable parallel function calling."""

    presence_penalty: Optional[float] = None
    """Penalize new tokens based on whether they appear in the text so far."""

    response_format: Optional[Dict[str, builtins.object]] = None
    """Format for the model output (e.g., {'type': 'json_object'})."""

    seed: Optional[int] = None
    """Seed for deterministic sampling."""

    service_tier: Optional[str] = None
    """Latency tier for the request (e.g., 'auto', 'default')."""

    stop: Union[str, List[str], None] = None
    """Up to 4 sequences where the API will stop generating further tokens."""

    stream: Optional[bool] = None
    """Whether to stream back partial progress."""

    stream_options: Optional[Dict[str, builtins.object]] = None
    """Options for streaming responses."""

    temperature: Optional[float] = None
    """Sampling temperature (0 to 2). Higher values make output more random."""

    tool_choice: Union[str, Dict[str, builtins.object], None] = None
    """Controls which tool is called by the model."""

    tools: Optional[List[Dict[str, builtins.object]]] = None
    """List of tools the model may call."""

    top_logprobs: Optional[int] = None
    """Number of most likely tokens to return at each token position."""

    top_p: Optional[float] = None
    """Nucleus sampling parameter. Alternative to temperature."""

    user: Optional[str] = None
    """A unique identifier representing your end-user."""
