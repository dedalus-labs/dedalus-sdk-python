# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .chunk_choice import ChunkChoice
from .completion_usage import CompletionUsage

__all__ = ["StreamChunk"]


class StreamChunk(BaseModel):
    id: str
    """Unique identifier for the chat completion"""

    choices: List[ChunkChoice]
    """List of completion choice chunks"""

    created: int
    """Unix timestamp when the chunk was created"""

    model: str
    """ID of the model used for the completion"""

    object: Optional[Literal["chat.completion.chunk"]] = None
    """Object type, always 'chat.completion.chunk'"""

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None
    """Service tier used for processing the request"""

    system_fingerprint: Optional[str] = None
    """System fingerprint representing backend configuration"""

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request.

    Fields:

    - completion_tokens (required): int
    - prompt_tokens (required): int
    - total_tokens (required): int
    - completion_tokens_details (optional): CompletionTokensDetails
    - prompt_tokens_details (optional): PromptTokensDetails
    """
