# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .completion import Completion
from .stream_chunk import StreamChunk

__all__ = ["ChatCreateResponse"]

ChatCreateResponse: TypeAlias = Union[Completion, StreamChunk]
