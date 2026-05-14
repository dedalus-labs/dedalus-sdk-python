"""Integration tests: `DedalusRunner` emits events to `on_model_event` / `on_tool_event`.

Uses respx to mock the HTTP boundary so these tests are hermetic and fast.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import httpx
import pytest
from respx import MockRouter

from dedalus_labs import Dedalus
from dedalus_labs.lib.replay import (
    FORMAT_VERSION,
    MODEL_REQUEST,
    MODEL_RESPONSE,
    TOOL_END,
    Recorder,
)
from dedalus_labs.lib.runner import DedalusRunner

from ..conftest import base_url


def _completion(
    *,
    content: str | None = None,
    tool_calls: List[Dict[str, Any]] | None = None,
    finish_reason: str = "stop",
) -> Dict[str, Any]:
    """Minimal mock chat-completion response shaped like the API."""
    message: Dict[str, Any] = {"role": "assistant"}
    if content is not None:
        message["content"] = content
    if tool_calls is not None:
        message["tool_calls"] = tool_calls
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 0,
        "model": "openai/gpt-5-nano",
        "choices": [{"index": 0, "message": message, "logprobs": None, "finish_reason": finish_reason}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    }


def _add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@pytest.mark.respx(base_url=base_url)
def test_runner_emits_model_request_then_response(client: Dedalus, respx_mock: MockRouter) -> None:
    """A no-tool response produces exactly one (request, response) pair."""
    respx_mock.post("/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=_completion(content="Hello there."))
    )

    events: List[Dict[str, Any]] = []
    runner = DedalusRunner(client)
    runner.run(
        model="openai/gpt-5-nano",
        input="hi",
        on_model_event=events.append,
    )

    kinds = [e["kind"] for e in events]
    assert kinds == [MODEL_REQUEST, MODEL_RESPONSE]
    assert events[0]["step"] == 1
    assert events[1]["step"] == 1
    assert events[1]["response"]["choices"][0]["message"]["content"] == "Hello there."


@pytest.mark.respx(base_url=base_url)
def test_runner_emits_tool_end_after_local_tool_runs(client: Dedalus, respx_mock: MockRouter) -> None:
    """A tool-calling turn produces a `tool_end` event with name + result + correlated id/args."""
    tool_call_payload = {
        "id": "call_xyz",
        "type": "function",
        "function": {"name": "_add", "arguments": json.dumps({"a": 3, "b": 4})},
    }
    respx_mock.post("/v1/chat/completions").mock(
        side_effect=[
            httpx.Response(200, json=_completion(tool_calls=[tool_call_payload], finish_reason="tool_calls")),
            httpx.Response(200, json=_completion(content="The answer is 7.")),
        ]
    )

    tool_events: List[Dict[str, Any]] = []
    runner = DedalusRunner(client)
    runner.run(
        model="openai/gpt-5-nano",
        input="What is 3 + 4?",
        tools=[_add],
        on_tool_event=tool_events.append,
    )

    assert len(tool_events) == 1
    event = tool_events[0]
    assert event["kind"] == TOOL_END
    assert event["name"] == "_add"
    assert event["result"] == 7
    assert event["tool_call_id"] == "call_xyz"
    # arguments are forwarded as the raw JSON string the model produced
    assert json.loads(event["arguments"]) == {"a": 3, "b": 4}


@pytest.mark.respx(base_url=base_url)
def test_runner_does_not_break_when_callback_raises(client: Dedalus, respx_mock: MockRouter) -> None:
    """A misbehaving callback must not propagate — the run completes normally."""
    respx_mock.post("/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=_completion(content="ok"))
    )

    def boom(_event: Dict[str, Any]) -> None:
        raise RuntimeError("callback intentionally broken")

    runner = DedalusRunner(client)
    result = runner.run(
        model="openai/gpt-5-nano",
        input="hi",
        on_model_event=boom,
        on_tool_event=boom,
    )
    assert result.final_output == "ok"


@pytest.mark.respx(base_url=base_url)
def test_tool_end_events_correlate_by_id_under_concurrency(
    client: Dedalus, respx_mock: MockRouter
) -> None:
    """Two concurrent calls to the same tool must map each tool_end to the right tool_call_id."""
    import asyncio

    # Two parallel calls to the same tool, distinguishable only by their arguments
    tc_fast = {
        "id": "call_fast",
        "type": "function",
        "function": {"name": "_slow_add", "arguments": json.dumps({"a": 1, "b": 1, "delay": 0.0})},
    }
    tc_slow = {
        "id": "call_slow",
        "type": "function",
        "function": {"name": "_slow_add", "arguments": json.dumps({"a": 10, "b": 10, "delay": 0.05})},
    }
    respx_mock.post("/v1/chat/completions").mock(
        side_effect=[
            httpx.Response(200, json=_completion(tool_calls=[tc_slow, tc_fast], finish_reason="tool_calls")),
            httpx.Response(200, json=_completion(content="done")),
        ]
    )

    async def _slow_add(a: int, b: int, delay: float = 0.0) -> int:
        await asyncio.sleep(delay)
        return a + b

    tool_events: List[Dict[str, Any]] = []
    runner = DedalusRunner(client)
    runner.run(
        model="openai/gpt-5-nano",
        input="parallel add",
        tools=[_slow_add],
        on_tool_event=tool_events.append,
    )

    assert len(tool_events) == 2
    # Each event must carry the ARGUMENTS that match its tool_call_id, not a swap caused by completion ordering
    by_id = {e["tool_call_id"]: e for e in tool_events}
    assert json.loads(by_id["call_fast"]["arguments"]) == {"a": 1, "b": 1, "delay": 0.0}
    assert json.loads(by_id["call_slow"]["arguments"]) == {"a": 10, "b": 10, "delay": 0.05}
    assert by_id["call_fast"]["result"] == 2
    assert by_id["call_slow"]["result"] == 20


@pytest.mark.respx(base_url=base_url)
def test_model_request_event_omits_credentials(client: Dedalus, respx_mock: MockRouter) -> None:
    """`credentials` must never reach the model_request event payload."""
    respx_mock.post("/v1/chat/completions").mock(
        return_value=httpx.Response(200, json=_completion(content="ok"))
    )

    events: List[Dict[str, Any]] = []
    runner = DedalusRunner(client)
    runner.run(
        model="openai/gpt-5-nano",
        input="hi",
        credentials=[{"provider": "openai", "api_key": "sk-secret-do-not-leak"}],
        on_model_event=events.append,
    )

    request_events = [e for e in events if e["kind"] == MODEL_REQUEST]
    assert request_events, "expected at least one model_request event"
    for ev in request_events:
        assert "credentials" not in ev["request"], (
            f"credentials field leaked into trace event: {ev['request']!r}"
        )
        # Defense in depth: the secret value must not appear anywhere serialized
        assert "sk-secret-do-not-leak" not in json.dumps(ev)


@pytest.mark.respx(base_url=base_url)
def test_record_then_load_produces_valid_trace_format(
    client: Dedalus, respx_mock: MockRouter, tmp_path: Path
) -> None:
    """End-to-end: record a full run via Recorder, reload the trace, validate the envelope."""
    tool_call_payload = {
        "id": "call_xyz",
        "type": "function",
        "function": {"name": "_add", "arguments": json.dumps({"a": 3, "b": 4})},
    }
    respx_mock.post("/v1/chat/completions").mock(
        side_effect=[
            httpx.Response(200, json=_completion(tool_calls=[tool_call_payload], finish_reason="tool_calls")),
            httpx.Response(200, json=_completion(content="The answer is 7.")),
        ]
    )

    trace_path = tmp_path / "trace.json"
    runner = DedalusRunner(client)
    with Recorder(trace_path, metadata={"test": True}) as rec:
        runner.run(
            model="openai/gpt-5-nano",
            input="What is 3 + 4?",
            tools=[_add],
            on_model_event=rec.on_model,
            on_tool_event=rec.on_tool,
        )

    trace = json.loads(trace_path.read_text(encoding="utf-8"))

    # Envelope shape
    assert trace["format_version"] == FORMAT_VERSION
    assert trace["sdk_version"]
    assert trace["recorded_at"].endswith("Z")
    assert trace["metadata"] == {"test": True}

    # Every event has the required keys
    for event in trace["events"]:
        assert "kind" in event and "step" in event and "ts" in event

    kinds = [e["kind"] for e in trace["events"]]
    # Two turns: request → response → tool_end → request → response
    assert kinds == [MODEL_REQUEST, MODEL_RESPONSE, TOOL_END, MODEL_REQUEST, MODEL_RESPONSE]
