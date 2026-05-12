"""Regression test: verbose=True must not crash on Pydantic tool_call objects.

Prior to the fix, several verbose-print sites in `runner/core.py` called
`tc.get(...)` on `ChatCompletionMessageToolCall` Pydantic objects, raising
`AttributeError`. This test drives a synthetic Pydantic response through
the verbose-print helpers and asserts no exception.
"""

from __future__ import annotations

from typing import Any

import pytest

from dedalus_labs.lib.runner.core import _tc_id, _tc_name


class _FakeFunction:
    def __init__(self, name: str) -> None:
        self.name = name


class _FakeToolCall:
    """Stand-in for ChatCompletionMessageToolCall — Pydantic-shaped (attrs, no .get)."""

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.function = _FakeFunction(name)


def test_tc_name_handles_dict_shape() -> None:
    tc: dict[str, Any] = {"id": "c1", "function": {"name": "add"}}
    assert _tc_name(tc) == "add"
    assert _tc_id(tc) == "c1"


def test_tc_name_handles_pydantic_shape() -> None:
    tc = _FakeToolCall(id="c1", name="add")
    assert _tc_name(tc) == "add"
    assert _tc_id(tc) == "c1"


def test_tc_name_default() -> None:
    assert _tc_name({}, default="unknown") == "unknown"
    assert _tc_id({}, default="zzz") == "zzz"

    class _Empty:
        pass

    assert _tc_name(_Empty(), default="unknown") == "unknown"
    assert _tc_id(_Empty(), default="zzz") == "zzz"


def test_tc_name_pydantic_raises_without_helper() -> None:
    """Sanity: confirms the original bug shape (Pydantic objects have no .get)."""
    tc = _FakeToolCall(id="c1", name="add")
    with pytest.raises(AttributeError):
        tc.get("function", {}).get("name", "?")  # type: ignore[attr-defined]
