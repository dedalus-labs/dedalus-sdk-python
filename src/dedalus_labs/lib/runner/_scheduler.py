# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Dependency-aware local tool scheduler.

When the API server returns ``pending_local_calls`` with dependency
info, this module topo-sorts and executes them in parallel layers.
Independent tools fire concurrently; dependent tools wait for their
prerequisites.

Falls back to sequential execution when dependencies form a cycle
(model hallucinated wrong deps).

Functions:
    execute_local_tools_async -- async path, uses asyncio.gather per layer
    execute_local_tools_sync  -- sync path, sequential within layers
"""

from __future__ import annotations

import json
import asyncio
from typing import Any, Dict, List, Tuple

from graphlib import CycleError, TopologicalSorter


def _parse_pending_calls(
    tool_calls: List[Dict[str, Any]],
) -> Tuple[Dict[str, Dict[str, Any]], TopologicalSorter]:
    """Parse pending local calls and build a TopologicalSorter.

    Returns (calls_by_id, sorter). Each entry in calls_by_id has
    the parsed function name and arguments ready for execution.

    Raises CycleError if dependencies are cyclic.
    """
    calls_by_id: Dict[str, Dict[str, Any]] = {}
    sorter: TopologicalSorter = TopologicalSorter()
    known_ids = {tc["id"] for tc in tool_calls if "id" in tc}

    for tc in tool_calls:
        call_id = tc.get("id", "")
        fn_name = tc["function"]["name"]
        fn_args_str = tc["function"]["arguments"]

        try:
            fn_args = json.loads(fn_args_str) if isinstance(fn_args_str, str) else fn_args_str
        except json.JSONDecodeError:
            fn_args = {}

        # Filter deps to only known ids in this batch.
        raw_deps = tc.get("dependencies") or []
        deps = [dep for dep in raw_deps if dep in known_ids and dep != call_id]

        calls_by_id[call_id] = {"name": fn_name, "args": fn_args, "id": call_id}
        sorter.add(call_id, *deps)

    sorter.prepare()
    return calls_by_id, sorter


async def execute_local_tools_async(
    tool_calls: List[Dict[str, Any]],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
    *,
    verbose: bool = False,
) -> None:
    """Execute local tool calls respecting dependencies (async).

    Independent tools within the same topo layer fire concurrently
    via asyncio.gather. Falls back to sequential on cycle.

    The caller is responsible for appending the assistant message
    (with tool_calls and any reasoning_content) before calling this.
    """
    if not tool_calls:
        return

    try:
        calls_by_id, sorter = _parse_pending_calls(tool_calls)
    except CycleError:
        # If wrong deps from model, fall back to sequential.
        await _execute_sequential_async(
            tool_calls,
            tool_handler,
            messages,
            tool_results,
            tools_called,
            step,
            verbose,
        )
        return

    # Drive the sorter layer by layer.
    while sorter.is_active():
        ready = list(sorter.get_ready())
        if not ready:
            break

        if len(ready) == 1:
            # Single tool: no gather overhead.
            call_id = ready[0]
            await _run_one_async(
                calls_by_id[call_id],
                tool_handler,
                messages,
                tool_results,
                tools_called,
                step,
                verbose,
            )
            sorter.done(call_id)
        else:
            # Multiple independent tools: fire concurrently.
            results = await asyncio.gather(
                *[
                    _run_one_async(
                        calls_by_id[call_id],
                        tool_handler,
                        messages,
                        tool_results,
                        tools_called,
                        step,
                        verbose,
                    )
                    for call_id in ready
                ],
                return_exceptions=True,
            )

            for call_id, result in zip(ready, results):
                if isinstance(result, Exception):
                    # Already recorded in messages by _run_one_async.
                    pass
                sorter.done(call_id)


def execute_local_tools_sync(
    tool_calls: List[Dict[str, Any]],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
) -> None:
    """Execute local tool calls respecting dependencies (sync).

    Executes in topo order, one at a time. No parallelism in sync mode,
    but ordering is correct.

    The caller is responsible for appending the assistant message
    (with tool_calls and any reasoning_content) before calling this.
    """
    if not tool_calls:
        return

    try:
        calls_by_id, sorter = _parse_pending_calls(tool_calls)
    except CycleError:
        _execute_sequential_sync(
            tool_calls,
            tool_handler,
            messages,
            tool_results,
            tools_called,
            step,
        )
        return

    while sorter.is_active():
        ready = list(sorter.get_ready())
        if not ready:
            break
        for call_id in ready:
            _run_one_sync(
                calls_by_id[call_id],
                tool_handler,
                messages,
                tool_results,
                tools_called,
                step,
            )
            sorter.done(call_id)


# --- Single tool execution ---


async def _run_one_async(
    call: Dict[str, Any],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
    verbose: bool,
) -> None:
    """Execute a single tool call and record results."""
    fn_name = call["name"]
    fn_args = call["args"]
    call_id = call["id"]

    try:
        result = await tool_handler.exec(fn_name, fn_args)
        tool_results.append({"name": fn_name, "result": result, "step": step, "tool_call_id": call_id})
        tools_called.append(fn_name)
        messages.append({"role": "tool", "tool_call_id": call_id, "content": str(result)})
        if verbose:
            print(f"  Tool {fn_name}: {str(result)[:50]}...")  # noqa: T201
    except Exception as e:
        tool_results.append({"error": str(e), "name": fn_name, "step": step, "tool_call_id": call_id})
        messages.append({"role": "tool", "tool_call_id": call_id, "content": f"Error: {e}"})
        if verbose:
            print(f"  Tool {fn_name} failed: {e}")  # noqa: T201


def _run_one_sync(
    call: Dict[str, Any],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
) -> None:
    """Execute a single tool call synchronously and record results."""
    fn_name = call["name"]
    fn_args = call["args"]
    call_id = call["id"]

    try:
        result = tool_handler.exec_sync(fn_name, fn_args)
        tool_results.append({"name": fn_name, "result": result, "step": step, "tool_call_id": call_id})
        tools_called.append(fn_name)
        messages.append({"role": "tool", "tool_call_id": call_id, "content": str(result)})
    except Exception as e:
        tool_results.append({"error": str(e), "name": fn_name, "step": step, "tool_call_id": call_id})
        messages.append({"role": "tool", "tool_call_id": call_id, "content": f"Error: {e}"})


# --- Sequential fallback ---


async def _execute_sequential_async(
    tool_calls: List[Dict[str, Any]],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
    verbose: bool,
) -> None:
    """Fallback: execute all tools sequentially (no dependency ordering)."""
    for tc in tool_calls:
        fn_name = tc["function"]["name"]
        fn_args_str = tc["function"]["arguments"]
        call_id = tc.get("id", "")
        try:
            fn_args = json.loads(fn_args_str) if isinstance(fn_args_str, str) else fn_args_str
        except json.JSONDecodeError:
            fn_args = {}

        call = {"name": fn_name, "args": fn_args, "id": call_id}
        await _run_one_async(call, tool_handler, messages, tool_results, tools_called, step, verbose)


def _execute_sequential_sync(
    tool_calls: List[Dict[str, Any]],
    tool_handler: Any,
    messages: List[Dict[str, Any]],
    tool_results: List[Dict[str, Any]],
    tools_called: List[str],
    step: int,
) -> None:
    """Fallback: execute all tools sequentially (no dependency ordering)."""
    for tc in tool_calls:
        fn_name = tc["function"]["name"]
        fn_args_str = tc["function"]["arguments"]
        call_id = tc.get("id", "")
        try:
            fn_args = json.loads(fn_args_str) if isinstance(fn_args_str, str) else fn_args_str
        except json.JSONDecodeError:
            fn_args = {}

        call = {"name": fn_name, "args": fn_args, "id": call_id}
        _run_one_sync(call, tool_handler, messages, tool_results, tools_called, step)
