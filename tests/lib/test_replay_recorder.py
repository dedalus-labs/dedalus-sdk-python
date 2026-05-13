"""Unit tests for `dedalus_labs.lib.replay.Recorder`.

These tests do not involve the runner — they feed events directly to the
recorder and inspect the resulting JSON file.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dedalus_labs.lib.replay import (
    FORMAT_VERSION,
    MODEL_REQUEST,
    MODEL_RESPONSE,
    TOOL_END,
    Recorder,
)


def _read_trace(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_recorder_captures_event_order(tmp_path: Path) -> None:
    """Events are written in the order they were observed and stamped."""
    path = tmp_path / "trace.json"
    with Recorder(path) as rec:
        rec.on_model({"kind": MODEL_REQUEST, "step": 1, "request": {"x": 1}})
        rec.on_tool({"kind": TOOL_END, "step": 1, "name": "add", "result": 7})
        rec.on_model({"kind": MODEL_RESPONSE, "step": 1, "response": {"id": "abc"}})

    trace = _read_trace(path)
    assert [e["kind"] for e in trace["events"]] == [
        MODEL_REQUEST,
        TOOL_END,
        MODEL_RESPONSE,
    ]
    for event in trace["events"]:
        assert isinstance(event["ts"], float)


def test_recorder_redacts_before_storing(tmp_path: Path) -> None:
    """A redactor that strips a known string must keep raw values out of the trace."""
    path = tmp_path / "trace.json"

    def redact(event: dict) -> dict:
        return {**event, "request": {"messages": "<scrubbed>"}}

    with Recorder(path, redact=redact) as rec:
        rec.on_model(
            {
                "kind": MODEL_REQUEST,
                "step": 1,
                "request": {"messages": "SECRET-CUSTOMER-DATA"},
            }
        )

    raw = path.read_text(encoding="utf-8")
    assert "SECRET-CUSTOMER-DATA" not in raw
    trace = _read_trace(path)
    assert trace["events"][0]["request"]["messages"] == "<scrubbed>"


def test_recorder_metadata_and_envelope_fields(tmp_path: Path) -> None:
    """User metadata round-trips and the envelope carries format/sdk version."""
    path = tmp_path / "trace.json"
    with Recorder(path, metadata={"ticket": "INC-42", "customer": "acme"}) as rec:
        rec.on_model({"kind": MODEL_REQUEST, "step": 1, "request": {}})

    trace = _read_trace(path)
    assert trace["format_version"] == FORMAT_VERSION
    assert trace["sdk_version"]  # truthy; exact value asserted elsewhere
    assert trace["metadata"] == {"ticket": "INC-42", "customer": "acme"}
    assert trace["recorded_at"].endswith("Z")


def test_recorder_context_manager_writes_on_exit(tmp_path: Path) -> None:
    """The trace file is created exactly when the `with` block exits."""
    path = tmp_path / "trace.json"
    rec = Recorder(path)
    rec.on_model({"kind": MODEL_REQUEST, "step": 1, "request": {}})
    assert not path.exists(), "file should not exist before save()"

    with rec:
        pass  # __exit__ calls save()

    assert path.exists()
    assert _read_trace(path)["events"][0]["kind"] == MODEL_REQUEST


def test_recorder_swallows_redactor_failure(tmp_path: Path) -> None:
    """A redactor that raises must not break recording. The event is kept and marked."""
    path = tmp_path / "trace.json"

    def broken(event: dict) -> dict:
        raise RuntimeError("boom")

    with Recorder(path, redact=broken) as rec:
        rec.on_model({"kind": MODEL_REQUEST, "step": 1, "request": {"k": "v"}})

    trace = _read_trace(path)
    assert trace["events"][0]["_redaction_failed"] is True
    assert trace["events"][0]["request"] == {"k": "v"}


def test_recorder_save_is_idempotent(tmp_path: Path) -> None:
    """Calling save() twice (or save() then __exit__) writes exactly once."""
    path = tmp_path / "trace.json"
    rec = Recorder(path)
    rec.on_model({"kind": MODEL_REQUEST, "step": 1, "request": {}})
    rec.save()
    first_mtime = path.stat().st_mtime_ns

    rec.save()  # idempotent
    assert path.stat().st_mtime_ns == first_mtime
