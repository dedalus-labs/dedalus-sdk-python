"""Tests for `dedalus_labs.lib.replay.Replayer` and `_fake_client`."""

from __future__ import annotations

import json
from typing import Any, Dict

import pytest

from dedalus_labs.lib.replay import FORMAT_VERSION, Replayer
from dedalus_labs.lib.replay._fake_client import _FakeClient
from dedalus_labs.types.chat import ChatCompletion


def _make_completion(content: str = "done") -> ChatCompletion:
    return ChatCompletion.model_validate(
        {
            "id": "chatcmpl-test",
            "object": "chat.completion",
            "created": 0,
            "model": "openai/gpt-5-nano",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        }
    )


class TestFakeClient:
    def test_create_pops_responses_in_order(self) -> None:
        r1 = _make_completion("first")
        r2 = _make_completion("second")
        client = _FakeClient([r1, r2])
        assert client.chat.completions.create() is r1
        assert client.chat.completions.create() is r2

    def test_create_raises_on_empty_queue(self) -> None:
        client = _FakeClient([])
        with pytest.raises(RuntimeError, match="replay drift"):
            client.chat.completions.create()

    def test_create_ignores_kwargs(self) -> None:
        r = _make_completion()
        client = _FakeClient([r])
        result = client.chat.completions.create(model="anything", messages=[])
        assert result is r


# ---------------------------------------------------------------------------
# Helpers shared by Replayer tests


def _completion_dict(content: str = "done", tool_calls: list[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    message: Dict[str, Any] = {"role": "assistant"}
    if content:
        message["content"] = content
    if tool_calls is not None:
        message["tool_calls"] = tool_calls
    finish_reason = "tool_calls" if tool_calls else "stop"
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 0,
        "model": "openai/gpt-5-nano",
        "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    }


def _minimal_trace(events: list[Dict[str, Any]]) -> Dict[str, Any]:
    return {"format_version": FORMAT_VERSION, "sdk_version": "0.3.0", "recorded_at": "2026-05-13T00:00:00Z", "metadata": {}, "events": events}


def _req_event(step: int = 1, tool_schemas: list[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    return {
        "kind": "model_request",
        "step": step,
        "ts": 0.0,
        "request": {
            "model": ["openai/gpt-5-nano"],
            "messages": [{"role": "user", "content": "What is 3 + 4?"}],
            "tools": tool_schemas or [],
            "mcp_servers": [],
        },
    }


def _resp_event(step: int = 1, content: str = "done", tool_calls: list[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    return {"kind": "model_response", "step": step, "ts": 0.0, "response": _completion_dict(content=content, tool_calls=tool_calls)}


def _tool_end_event(name: str, result: Any, step: int = 1, call_id: str = "call_1", error: str | None = None) -> Dict[str, Any]:
    ev: Dict[str, Any] = {
        "kind": "tool_end",
        "step": step,
        "ts": 0.0,
        "name": name,
        "tool_call_id": call_id,
        "arguments": json.dumps({"a": 3, "b": 4}),
        "result": result,
    }
    if error is not None:
        ev["error"] = error
    return ev


# ---------------------------------------------------------------------------
# Replayer tests


class TestReplayer:
    def test_unknown_format_version_rejected(self) -> None:
        with pytest.raises(ValueError, match="unsupported trace format_version"):
            Replayer.from_dict({"format_version": "9.9", "events": []})

    def test_missing_events_rejected(self) -> None:
        with pytest.raises(ValueError, match="missing an `events` list"):
            Replayer.from_dict({"format_version": FORMAT_VERSION})

    def test_round_trip_identity_no_tools(self) -> None:
        """Single turn with no tool calls: final output matches the recorded response."""
        trace = _minimal_trace([
            _req_event(),
            _resp_event(content="The answer is 7."),
        ])
        result = Replayer.from_dict(trace).run()
        assert result.final_output == "The answer is 7."

    def test_round_trip_with_tool_call(self) -> None:
        """Two-turn trace: model calls a tool, then gives a final answer."""
        tool_call = {"id": "call_1", "type": "function", "function": {"name": "add", "arguments": json.dumps({"a": 3, "b": 4})}}
        trace = _minimal_trace([
            _req_event(step=1),
            _resp_event(step=1, content="", tool_calls=[tool_call]),
            _tool_end_event("add", result=7, step=1),
            _req_event(step=2),
            _resp_event(step=2, content="The answer is 7."),
        ])
        result = Replayer.from_dict(trace).run()
        assert result.final_output == "The answer is 7."

    def test_swap_tool_runs_real_function(self) -> None:
        """swap_tool replaces the recorded stub with the provided callable."""
        called_with: list[Dict[str, Any]] = []

        def real_add(**kwargs: Any) -> int:
            called_with.append(kwargs)
            return 100

        tool_call = {"id": "call_1", "type": "function", "function": {"name": "add", "arguments": json.dumps({"a": 3, "b": 4})}}
        trace = _minimal_trace([
            _req_event(step=1),
            _resp_event(step=1, content="", tool_calls=[tool_call]),
            _tool_end_event("add", result=7, step=1),
            _req_event(step=2),
            _resp_event(step=2, content="done"),
        ])
        Replayer.from_dict(trace).run(swap_tool={"add": real_add})
        assert called_with, "real_add should have been called"

    def test_swap_client_bypasses_fake_client(self) -> None:
        """swap_client routes model calls to the provided object instead."""
        call_count = 0

        class StubCompletions:
            def create(self, **kwargs: Any) -> ChatCompletion:
                nonlocal call_count
                call_count += 1
                return _make_completion("stub answer")

        class StubChat:
            completions = StubCompletions()

        class StubClient:
            chat = StubChat()

        trace = _minimal_trace([_req_event(), _resp_event(content="original")])
        result = Replayer.from_dict(trace).run(swap_client=StubClient())
        assert call_count >= 1
        assert result.final_output == "stub answer"

    def test_drift_more_model_calls_than_recorded_raises(self) -> None:
        """If the runner needs more model responses than recorded, raise clearly."""
        tool_call = {"id": "call_1", "type": "function", "function": {"name": "add", "arguments": "{}"}}
        trace = _minimal_trace([
            _req_event(step=1),
            _resp_event(step=1, content="", tool_calls=[tool_call]),
            _tool_end_event("add", result=7, step=1),
            # deliberately omit the second model_response
        ])
        with pytest.raises(RuntimeError, match="replay drift"):
            Replayer.from_dict(trace).run()
