# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .stream_choice import StreamChoice
from .completion_usage import CompletionUsage

__all__ = ["ChatCompletionChunk"]


class ChatCompletionChunk(BaseModel):
    """
    Represents a streamed chunk of a chat completion response returned
    by the model, based on the provided input.
    [Learn more](https://platform.openai.com/docs/guides/streaming-responses).

    Fields:
    - id (required): str
    - choices (required): list[ChatCompletionStreamResponseChoicesItem]
    - created (required): int
    - model (required): str
    - service_tier (optional): ServiceTier
    - system_fingerprint (optional): str
    - object (required): Literal["chat.completion.chunk"]
    - usage (optional): CompletionUsage
    """

    id: str
    """A unique identifier for the chat completion. Each chunk has the same ID."""

    choices: List[StreamChoice]
    """A list of chat completion choices.

    Can contain more than one elements if `n` is greater than 1. Can also be empty
    for the last chunk if you set `stream_options: {"include_usage": true}`.
    """

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created.

    Each chunk has the same timestamp.
    """

    model: str
    """The model to generate the completion."""

    object: Literal["chat.completion.chunk"]
    """The object type, which is always `chat.completion.chunk`."""

    service_tier: Optional[Literal["auto", "default", "flex", "scale", "priority"]] = None
    """Specifies the processing type used for serving the request.

    - If set to 'auto', then the request will be processed with the service tier
      configured in the Project settings. Unless otherwise configured, the Project
      will use 'default'.
    - If set to 'default', then the request will be processed with the standard
      pricing and performance for the selected model.
    - If set to '[flex](https://platform.openai.com/docs/guides/flex-processing)' or
      '[priority](https://openai.com/api-priority-processing/)', then the request
      will be processed with the corresponding service tier.
    - When not set, the default behavior is 'auto'.

    When the `service_tier` parameter is set, the response body will include the
    `service_tier` value based on the processing mode actually used to serve the
    request. This response value may be different from the value set in the
    parameter.
    """

    system_fingerprint: Optional[str] = None
    """
    This fingerprint represents the backend configuration that the model runs with.
    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request.

    Fields:

    - completion_tokens (required): int
    - prompt_tokens (required): int
    - total_tokens (required): int
    - completion_tokens_details (optional): CompletionTokensDetails
    - prompt_tokens_details (optional): PromptTokensDetails
    """
