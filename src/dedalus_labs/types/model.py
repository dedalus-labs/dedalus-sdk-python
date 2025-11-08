# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Model", "Capabilities", "Defaults"]


class Capabilities(BaseModel):
    audio: Optional[bool] = None
    """Supports audio processing"""

    image_generation: Optional[bool] = None
    """Supports image generation"""

    input_token_limit: Optional[int] = None
    """Maximum input tokens"""

    output_token_limit: Optional[int] = None
    """Maximum output tokens"""

    streaming: Optional[bool] = None
    """Supports streaming responses"""

    structured_output: Optional[bool] = None
    """Supports structured JSON output"""

    text: Optional[bool] = None
    """Supports text generation"""

    thinking: Optional[bool] = None
    """Supports extended thinking/reasoning"""

    tools: Optional[bool] = None
    """Supports function/tool calling"""

    vision: Optional[bool] = None
    """Supports image understanding"""


class Defaults(BaseModel):
    max_output_tokens: Optional[int] = None
    """Default maximum output tokens"""

    temperature: Optional[float] = None
    """Default temperature setting"""

    top_k: Optional[int] = None
    """Default top_k setting"""

    top_p: Optional[float] = None
    """Default top_p setting"""


class Model(BaseModel):
    id: str
    """Unique model identifier with provider prefix (e.g., 'openai/gpt-4')"""

    created_at: datetime
    """When the model was released (RFC 3339)"""

    provider: Literal["openai", "anthropic", "google", "xai", "mistral", "groq", "fireworks", "deepseek"]
    """Provider that hosts this model"""

    capabilities: Optional[Capabilities] = None
    """Normalized model capabilities across all providers."""

    defaults: Optional[Defaults] = None
    """Provider-declared default parameters for model generation."""

    description: Optional[str] = None
    """Model description"""

    display_name: Optional[str] = None
    """Human-readable model name"""

    provider_declared_generation_methods: Optional[List[str]] = None
    """Provider-specific generation method names (None = not declared)"""

    provider_info: Optional[Dict[str, object]] = None
    """Raw provider-specific metadata"""

    version: Optional[str] = None
    """Model version identifier"""
