# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import os
from dataclasses import dataclass, field
from collections.abc import AsyncIterator, Iterator
from typing import Any, Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from ...types.chat.stream_chunk import StreamChunk

__all__ = [
    "StreamResult",
    "accumulate_tool_call",
    "stream_async",
    "stream_sync",
]


@dataclass
class StreamResult:
    """Collected data from a consumed stream.

    Returned by :func:`stream_async` and :func:`stream_sync` so callers
    can inspect what happened after the stream is exhausted.
    """

    content: str = ""
    """Concatenated text content from all ``delta.content`` fragments."""

    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    """Reassembled tool calls accumulated from streaming deltas.

    Each entry has the shape ``{"id": str, "function": {"name": str, "arguments": str}}``.
    """


def accumulate_tool_call(
    tool_calls: List[Dict[str, Any]],
    tc_delta: object,
) -> None:
    """Accumulate a single streaming tool-call delta into *tool_calls*.

    Reassembles the incremental fragments (id, function name, argument
    chunks, thought_signature) that arrive across multiple SSE chunks
    into complete tool-call dicts keyed by ``tc_delta.index``.

    This is the canonical implementation shared by both the stream
    helpers and :class:`~dedalus_labs.lib.runner.core.DedalusRunner`.
    """
    idx: int = getattr(tc_delta, "index", 0)
    while len(tool_calls) <= idx:
        tool_calls.append({"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
    entry = tool_calls[idx]

    tc_id = getattr(tc_delta, "id", None)
    if tc_id:
        entry["id"] = tc_id

    fn = getattr(tc_delta, "function", None)
    if fn is not None:
        if getattr(fn, "name", None):
            entry["function"]["name"] = fn.name
        if getattr(fn, "arguments", None):
            entry["function"]["arguments"] += fn.arguments

    thought_sig = getattr(tc_delta, "thought_signature", None)
    if thought_sig:
        entry["thought_signature"] = thought_sig


def _process_chunk(
    chunk: object,
    result: StreamResult,
    verbose: bool,
) -> None:
    """Extract content and tool-call deltas from a single StreamChunk."""
    if verbose:
        extra = getattr(chunk, "__pydantic_extra__", None)
        if isinstance(extra, dict):
            meta = extra.get("dedalus_event")
            if isinstance(meta, dict):
                print(f"\n[EVENT] {meta}")

    choices = getattr(chunk, "choices", None)
    if not choices:
        return

    choice = choices[0]
    delta = choice.delta

    # Tool-call deltas
    for tc in getattr(delta, "tool_calls", None) or []:
        if verbose:
            fn = getattr(tc, "function", None)
            print(f"\n[TOOL_CALL] name={getattr(fn, 'name', None)} id={getattr(tc, 'id', None)}")
        accumulate_tool_call(result.tool_calls, tc)

    # Content
    if delta.content:
        print(delta.content, end="", flush=True)
        result.content += delta.content

    # Finish reason (verbose-only)
    if verbose and getattr(choice, "finish_reason", None):
        print(f"\n[FINISH] reason={choice.finish_reason}")


async def stream_async(stream: AsyncIterator[StreamChunk] | object) -> StreamResult:
    """Stream text content from an async streaming response.

    Prints content tokens to stdout as they arrive **and** returns a
    :class:`StreamResult` with the accumulated content and tool calls.

    Supports both:
    - Raw StreamChunk iterator from .create(stream=True) or DedalusRunner.run(stream=True)
    - ChatCompletionStreamManager from .stream() (Pydantic models with event API)

    Args:
        stream: An async iterator of StreamChunk or a ChatCompletionStreamManager

    Returns:
        A :class:`StreamResult` containing the full content and any tool calls.

    Example:
        >>> stream = runner.run(input="...", model="...", stream=True)
        >>> result = await stream_async(stream)
        >>> print(result.tool_calls)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")
    result = StreamResult()

    # Stream manager (event API) vs raw AsyncStream: discriminate via __aenter__ without __aiter__
    if hasattr(stream, "__aenter__") and not hasattr(stream, "__aiter__"):
        async with stream as event_stream:
            async for event in event_stream:
                if event.type == "content.delta":
                    print(event.delta, end="", flush=True)
                    result.content += event.delta
                elif verbose and event.type == "content.done" and hasattr(event, "parsed") and event.parsed:
                    print(f"\n[PARSED] {type(event.parsed).__name__}")
        print()  # Final newline
        return result

    # Simple StreamChunk iterator case
    async for chunk in stream:
        _process_chunk(chunk, result, verbose)
    print()  # Final newline
    return result


def stream_sync(stream: Iterator[StreamChunk] | object) -> StreamResult:
    """Stream text content from a streaming response.

    Prints content tokens to stdout as they arrive **and** returns a
    :class:`StreamResult` with the accumulated content and tool calls.

    Supports both:
    - Raw StreamChunk iterator from .create(stream=True) or DedalusRunner.run(stream=True)
    - ChatCompletionStreamManager from .stream() (Pydantic models with event API)

    Args:
        stream: An iterator of StreamChunk or a ChatCompletionStreamManager

    Returns:
        A :class:`StreamResult` containing the full content and any tool calls.

    Example:
        >>> stream = runner.run(input="...", model="...", stream=True)
        >>> result = stream_sync(stream)
        >>> print(result.tool_calls)
    """
    verbose = os.environ.get("DEDALUS_SDK_VERBOSE", "").lower() in ("1", "true", "yes", "on", "debug")
    result = StreamResult()

    # Stream manager (event API) vs raw Stream: discriminate via __enter__ without __iter__
    if hasattr(stream, "__enter__") and not hasattr(stream, "__iter__"):
        with stream as event_stream:
            for event in event_stream:
                if event.type == "content.delta":
                    print(event.delta, end="", flush=True)
                    result.content += event.delta
                elif verbose and event.type == "content.done" and hasattr(event, "parsed") and event.parsed:
                    print(f"\n[PARSED] {type(event.parsed).__name__}")
        print()  # Final newline
        return result

    # Simple StreamChunk iterator case
    for chunk in stream:
        _process_chunk(chunk, result, verbose)
    print()  # Final newline
    return result
