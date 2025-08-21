# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator

if TYPE_CHECKING:
    from ...types.chat.stream_chunk import StreamChunk

__all__ = [
    "stream_sync",
    "stream_async",
]


async def stream_async(stream: AsyncIterator[StreamChunk]) -> None:
    """Stream text content from an async streaming response.
    
    Handles the common pattern of printing text deltas from a streaming response.
    
    Args:
        stream: An async iterator of StreamChunk from DedalusRunner.run(stream=True)
        
    Example:
        >>> result = await runner.run("Hello", stream=True)
        >>> await stream_async(result)

    """
    async for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="", flush=True)
    print()  # Final newline


def stream_sync(stream: Iterator[StreamChunk]) -> None:
    """Stream text content from a streaming response.
    
    Handles the common pattern of printing text deltas from a streaming response.
    
    Args:
        stream: An iterator of StreamChunk from DedalusRunner.run(stream=True)
        
    Example:
        >>> result = runner.run("Hello", stream=True)
        >>> stream_sync(result)

    """
    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="", flush=True)
    print()  # Final newline
