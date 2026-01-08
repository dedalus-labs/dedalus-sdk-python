# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .chat_completion_token_logprob import ChatCompletionTokenLogprob

__all__ = ["StreamChoiceLogprobs"]


class StreamChoiceLogprobs(BaseModel):
    """Log probability information for the choice.

    Fields:
    - content (required): list[ChatCompletionTokenLogprob]
    - refusal (required): list[ChatCompletionTokenLogprob]
    """

    content: Optional[List[ChatCompletionTokenLogprob]] = None
    """A list of message content tokens with log probability information."""

    refusal: Optional[List[ChatCompletionTokenLogprob]] = None
    """A list of message refusal tokens with log probability information."""
