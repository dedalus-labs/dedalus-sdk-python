# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

from ..._models import BaseModel

__all__ = ["DedalusModel"]


class DedalusModel(BaseModel):
    """Structured model selection entry used in request payloads.

    Supports OpenAI-style semantics (string model id) while enabling
    optional per-model default settings for Dedalus multi-model routing.
    """

    model: str
    """
    Model identifier with provider prefix (e.g., 'openai/gpt-5',
    'anthropic/claude-3-5-sonnet').
    """

    settings: Optional["ModelSettings"] = None
    """
    Optional default generation settings (e.g., temperature, max_tokens) applied
    when this model is selected.
    """


from .model_settings import ModelSettings
