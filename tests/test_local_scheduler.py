# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for SDK-side dependency-aware local tool scheduler."""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

import pytest

from dedalus_labs.lib.runner._scheduler import (
    execute_local_tools_async,
    execute_local_tools_sync,
)


# --- Test helpers ---


def _make_tool_call(
    call_id: str,
    name: str,
    args: Dict[str, Any] | None = None,
    dependencies: list[str] | None = None,
) -> Dict[str, Any]:
    """Build a tool call dict matching the format from core.py."""
    return {
        "id": call_id,
        "type": "function",
        "function": {
            "name": name,
            "arguments": json.dumps(args or {}),
        },
        "dependencies": dependencies or [],
    }


def _make_async_handler(
    results: Dict[str, Any] | None = None,
    delay: float = 0.0,
) -> AsyncMock:
    """Create a mock tool handler with async exec."""
    handler = MagicMock()
    results = results or {}

    async def exec_fn(name: str, args: Dict[str, Any]) -> Any:
        if delay:
            await asyncio.sleep(delay)
        if name in results:
            return results[name]
        return f"result_{name}"

    handler.exec = AsyncMock(side_effect=exec_fn)
    return handler


def _make_sync_handler(results: Dict[str, Any] | None = None) -> MagicMock:
    """Create a mock tool handler with sync exec_sync."""
    handler = MagicMock()
    results = results or {}

    def exec_sync_fn(name: str, args: Dict[str, Any]) -> Any:
        if name in results:
            return results[name]
        return f"result_{name}"

    handler.exec_sync = MagicMock(side_effect=exec_sync_fn)
    return handler


# --- Async tests ---


@pytest.mark.asyncio
async def test_async_independent_tools_run_in_parallel():
    """Independent tools with no deps fire concurrently."""
    handler = _make_async_handler(delay=0.05)
    calls = [
        _make_tool_call("a", "fetch_a"),
        _make_tool_call("b", "fetch_b"),
        _make_tool_call("c", "fetch_c"),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    start = time.monotonic()
    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    elapsed = time.monotonic() - start

    assert len(tools_called) == 3
    # Parallel: should complete in ~1x delay, not 3x.
    assert elapsed < 0.15


@pytest.mark.asyncio
async def test_async_chain_respects_ordering():
    """b depends on a: a executes before b."""
    execution_order: list[str] = []
    handler = MagicMock()

    async def tracking_exec(name: str, args: Dict[str, Any]) -> str:
        execution_order.append(name)
        return f"done_{name}"

    handler.exec = AsyncMock(side_effect=tracking_exec)

    calls = [
        _make_tool_call("a", "fetch"),
        _make_tool_call("b", "transform", dependencies=["a"]),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    assert execution_order == ["fetch", "transform"]


@pytest.mark.asyncio
async def test_async_diamond_dependency():
    """Diamond: a,b independent, c depends on both."""
    execution_order: list[str] = []
    handler = MagicMock()

    async def tracking_exec(name: str, args: Dict[str, Any]) -> str:
        execution_order.append(name)
        return f"done_{name}"

    handler.exec = AsyncMock(side_effect=tracking_exec)

    calls = [
        _make_tool_call("a", "fetch_a"),
        _make_tool_call("b", "fetch_b"),
        _make_tool_call("c", "combine", dependencies=["a", "b"]),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    # a and b execute first (any order), then c.
    assert execution_order[-1] == "combine"
    assert set(execution_order[:2]) == {"fetch_a", "fetch_b"}


@pytest.mark.asyncio
async def test_async_cycle_falls_back_to_sequential():
    """Cyclic deps don't crash. Falls back to sequential execution."""
    handler = _make_async_handler()
    calls = [
        _make_tool_call("a", "fetch", dependencies=["b"]),
        _make_tool_call("b", "fetch", dependencies=["a"]),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    assert len(tools_called) == 2


@pytest.mark.asyncio
async def test_async_records_messages_correctly():
    """Tool results are recorded as messages in correct format."""
    handler = _make_async_handler(results={"my_tool": "hello world"})
    calls = [_make_tool_call("call_1", "my_tool", args={"x": 1})]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)

    # Scheduler only appends tool result messages (assistant message is caller's job).
    assert messages[0]["role"] == "tool"
    assert messages[0]["tool_call_id"] == "call_1"
    assert messages[0]["content"] == "hello world"


@pytest.mark.asyncio
async def test_async_tool_error_recorded():
    """Tool execution errors are recorded in messages, not raised."""
    handler = MagicMock()

    async def failing_exec(name: str, args: Dict[str, Any]) -> str:
        raise RuntimeError("boom")

    handler.exec = AsyncMock(side_effect=failing_exec)
    calls = [_make_tool_call("a", "bad_tool")]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    assert "error" in tool_results[0]
    assert messages[0]["content"] == "Error: boom"


@pytest.mark.asyncio
async def test_async_empty_calls():
    """Empty call list is a no-op."""
    handler = _make_async_handler()
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async([], handler, messages, tool_results, tools_called, step=1)
    assert messages == []


@pytest.mark.asyncio
async def test_async_unknown_deps_ignored():
    """Dependencies referencing ids not in this batch are filtered."""
    handler = _make_async_handler()
    calls = [_make_tool_call("a", "fetch", dependencies=["nonexistent"])]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    await execute_local_tools_async(calls, handler, messages, tool_results, tools_called, step=1)
    assert len(tools_called) == 1


# --- Sync tests ---


def test_sync_chain_respects_ordering():
    """Sync path: b depends on a, executes in correct order."""
    execution_order: list[str] = []
    handler = MagicMock()

    def tracking_sync(name: str, args: Dict[str, Any]) -> str:
        execution_order.append(name)
        return f"done_{name}"

    handler.exec_sync = MagicMock(side_effect=tracking_sync)

    calls = [
        _make_tool_call("a", "fetch"),
        _make_tool_call("b", "transform", dependencies=["a"]),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    execute_local_tools_sync(calls, handler, messages, tool_results, tools_called, step=1)
    assert execution_order == ["fetch", "transform"]


def test_sync_cycle_falls_back():
    """Sync path: cycle detected, falls back to sequential."""
    handler = _make_sync_handler()
    calls = [
        _make_tool_call("a", "fetch", dependencies=["b"]),
        _make_tool_call("b", "fetch", dependencies=["a"]),
    ]
    messages: list = []
    tool_results: list = []
    tools_called: list = []

    execute_local_tools_sync(calls, handler, messages, tool_results, tools_called, step=1)
    assert len(tools_called) == 2


def test_sync_empty_calls():
    """Sync path: empty call list is a no-op."""
    handler = _make_sync_handler()
    messages: list = []
    execute_local_tools_sync([], handler, messages, [], [], step=1)
    assert messages == []
