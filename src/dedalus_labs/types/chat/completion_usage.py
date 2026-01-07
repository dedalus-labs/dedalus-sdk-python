# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel
from .prompt_tokens_details import PromptTokensDetails
from .completion_tokens_details import CompletionTokensDetails

__all__ = ["CompletionUsage"]


class CompletionUsage(BaseModel):
    """Usage statistics for the completion request.

    Fields:
    - completion_tokens (required): int
    - prompt_tokens (required): int
    - total_tokens (required): int
    - completion_tokens_details (optional): CompletionTokensDetails
    - prompt_tokens_details (optional): PromptTokensDetails
    """

    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""

    completion_tokens_details: Optional[CompletionTokensDetails] = None
    """Breakdown of tokens used in a completion."""

    prompt_tokens_details: Optional[PromptTokensDetails] = None
    """Breakdown of tokens used in the prompt."""
