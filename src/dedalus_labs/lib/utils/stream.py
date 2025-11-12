# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator
import os

if TYPE_CHECKING:
    from ...types.chat.stream_chunk import StreamChunk

__all__ = [
    "stream_sync",
    "stream_async",
]


async def stream_async(stream: AsyncIterator[StreamChunk] | object) -> None:
    """Stream text content from an async streaming response.

    Supports both:
    - Raw StreamChunk iterator from .create(stream=True) or DedalusRunner.run(stream=True)
    - ChatCompletionStreamManager from .stream() (Pydantic models with event API)

    Args:
        stream: An async iterator of StreamChunk or a ChatCompletionStreamManager

    Example:
        >>> # With .create(stream=True)
        >>> stream = await client.chat.completions.create(stream=True, ...)
        >>> await stream_async(stream)

        >>> # With .stream() (Pydantic models)
        >>> stream = client.chat.completions.stream(response_format=Model, ...)
        >>> await stream_async(stream)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")

    # Check if it's a ChatCompletionStreamManager (context manager with event API)
    if hasattr(stream, "__aenter__"):
        async with stream as event_stream:
            async for event in event_stream:
                if event.type == "content.delta":
                    print(event.delta, end="", flush=True)
                elif verbose and event.type == "content.done":
                    if hasattr(event, "parsed") and event.parsed:
                        print(f"\n[PARSED] {type(event.parsed).__name__}")
        print()  # Final newline
        return

    # Simple StreamChunk iterator case
    async for chunk in stream:
        # Print server-side metadata events if present (verbose-only)
        if verbose:
            extra = getattr(chunk, "__pydantic_extra__", None)
            if isinstance(extra, dict):
                meta = extra.get("dedalus_event")
                if isinstance(meta, dict):
                    print(f"\n[EVENT] {meta}")

        if chunk.choices:
            choice = chunk.choices[0]
            delta = choice.delta
            # Print tool-call deltas as debug (verbose-only)
            if verbose and getattr(delta, "tool_calls", None):
                for tc in delta.tool_calls:
                    fn = getattr(tc, "function", None)
                    name = getattr(fn, "name", None)
                    tcid = getattr(tc, "id", None)
                    print(f"\n[TOOL_CALL] name={name} id={tcid}")
            # Always print content
            if delta.content:
                print(delta.content, end="", flush=True)
            # Print finish reason (verbose-only)
            if verbose and getattr(choice, "finish_reason", None):
                print(f"\n[FINISH] reason={choice.finish_reason}")
    print()  # Final newline


def stream_sync(stream: Iterator[StreamChunk] | object) -> None:
    """Stream text content from a streaming response.

    Supports both:
    - Raw StreamChunk iterator from .create(stream=True) or DedalusRunner.run(stream=True)
    - ChatCompletionStreamManager from .stream() (Pydantic models with event API)

    Args:
        stream: An iterator of StreamChunk or a ChatCompletionStreamManager

    Example:
        >>> # With .create(stream=True)
        >>> stream = client.chat.completions.create(stream=True, ...)
        >>> stream_sync(stream)

        >>> # With .stream() (Pydantic models)
        >>> stream = client.chat.completions.stream(response_format=Model, ...)
        >>> stream_sync(stream)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")

    # Check if it's a ChatCompletionStreamManager (context manager with event API)
    if hasattr(stream, "__enter__"):
        with stream as event_stream:
            for event in event_stream:
                if event.type == "content.delta":
                    print(event.delta, end="", flush=True)
                elif verbose and event.type == "content.done":
                    if hasattr(event, "parsed") and event.parsed:
                        print(f"\n[PARSED] {type(event.parsed).__name__}")
        print()  # Final newline
        return

    # Simple StreamChunk iterator case
    for chunk in stream:
        # Print server-side metadata events if present (verbose-only)
        if verbose:
            extra = getattr(chunk, "__pydantic_extra__", None)
            if isinstance(extra, dict):
                meta = extra.get("dedalus_event")
                if isinstance(meta, dict):
                    print(f"\n[EVENT] {meta}")

        if chunk.choices:
            choice = chunk.choices[0]
            delta = choice.delta
            # Print tool-call deltas as debug (verbose-only)
            if verbose and getattr(delta, "tool_calls", None):
                for tc in delta.tool_calls:
                    fn = getattr(tc, "function", None)
                    name = getattr(fn, "name", None)
                    tcid = getattr(tc, "id", None)
                    print(f"\n[TOOL_CALL] name={name} id={tcid}")
            # Always print content
            if delta.content:
                print(delta.content, end="", flush=True)
            if verbose and getattr(choice, "finish_reason", None):
                print(f"\n[FINISH] reason={choice.finish_reason}")
    print()  # Final newline
