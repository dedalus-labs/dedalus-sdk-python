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


async def stream_async(stream: AsyncIterator[StreamChunk]) -> None:
    """Stream text content from an async streaming response.

    Args:
        stream: An async iterator of StreamChunk from DedalusRunner.run(stream=True)

    Example:
        >>> result = await runner.run("Hello", stream=True)
        >>> await stream_async(result)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")

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


def stream_sync(stream: Iterator[StreamChunk]) -> None:
    """Stream text content from a streaming response.

    Args:
        stream: An iterator of StreamChunk from DedalusRunner.run(stream=True)

    Example:
        >>> result = runner.run("Hello", stream=True)
        >>> stream_sync(result)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")

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
