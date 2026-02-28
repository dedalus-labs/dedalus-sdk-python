# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for stream helpers: accumulate_tool_call, stream_async, stream_sync."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, AsyncIterator, List

import pytest

from dedalus_labs.lib.utils._stream import StreamResult, accumulate_tool_call, stream_async, stream_sync


# --- Test helpers ---


def _chunk(
    *,
    content: str | None = None,
    tool_calls: List[Any] | None = None,
    finish_reason: str | None = None,
) -> SimpleNamespace:
    delta = SimpleNamespace(content=content, tool_calls=tool_calls)
    choice = SimpleNamespace(delta=delta, finish_reason=finish_reason)
    return SimpleNamespace(choices=[choice])


def _tc(
    index: int,
    *,
    tc_id: str | None = None,
    name: str | None = None,
    arguments: str | None = None,
    thought_signature: str | None = None,
) -> SimpleNamespace:
    fn = SimpleNamespace(name=name, arguments=arguments)
    ns = SimpleNamespace(index=index, id=tc_id, function=fn)
    if thought_signature is not None:
        ns.thought_signature = thought_signature
    return ns


async def _aiter(items: list) -> AsyncIterator:
    for item in items:
        yield item


# --- accumulate_tool_call ---


def test_accumulate_creates_entry():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(0, tc_id="call_1", name="search"))
    assert acc == [{"id": "call_1", "type": "function", "function": {"name": "search", "arguments": ""}}]


def test_accumulate_appends_arguments():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(0, tc_id="c", name="fn"))
    accumulate_tool_call(acc, _tc(0, arguments='{"a":'))
    accumulate_tool_call(acc, _tc(0, arguments=" 1}"))
    assert acc[0]["function"]["arguments"] == '{"a": 1}'


def test_accumulate_parallel_indices():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(0, tc_id="c0", name="alpha"))
    accumulate_tool_call(acc, _tc(1, tc_id="c1", name="beta"))
    assert len(acc) == 2
    assert acc[0]["function"]["name"] == "alpha"
    assert acc[1]["function"]["name"] == "beta"


def test_accumulate_sparse_index_pads():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(2, tc_id="c2", name="gamma"))
    assert len(acc) == 3
    assert acc[2]["function"]["name"] == "gamma"
    assert acc[0]["function"]["name"] == ""


def test_accumulate_thought_signature():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(0, tc_id="c", name="fn", thought_signature="sig_abc"))
    assert acc[0]["thought_signature"] == "sig_abc"


def test_accumulate_no_thought_signature():
    acc: list[dict] = []
    accumulate_tool_call(acc, _tc(0, tc_id="c", name="fn"))
    assert "thought_signature" not in acc[0]


# --- stream_async ---


@pytest.mark.asyncio
async def test_async_content_only(capsys: pytest.CaptureFixture[str]):
    result = await stream_async(_aiter([_chunk(content="Hello"), _chunk(content=" world")]))
    assert isinstance(result, StreamResult)
    assert result.content == "Hello world"
    assert result.tool_calls == []
    assert "Hello world" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_async_empty():
    result = await stream_async(_aiter([]))
    assert result.content == ""
    assert result.tool_calls == []


@pytest.mark.asyncio
async def test_async_reassembles_tool_call():
    chunks = [
        _chunk(tool_calls=[_tc(0, tc_id="call_abc", name="gmail_send")]),
        _chunk(tool_calls=[_tc(0, arguments='{"to":')]),
        _chunk(tool_calls=[_tc(0, arguments=' "a@b.com"}')]),
        _chunk(content="Sent.", finish_reason="stop"),
    ]
    result = await stream_async(_aiter(chunks))
    assert result.content == "Sent."
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0]["id"] == "call_abc"
    assert result.tool_calls[0]["type"] == "function"
    assert result.tool_calls[0]["function"] == {"name": "gmail_send", "arguments": '{"to": "a@b.com"}'}


@pytest.mark.asyncio
async def test_async_parallel_tool_calls():
    chunks = [
        _chunk(tool_calls=[_tc(0, tc_id="c1", name="search"), _tc(1, tc_id="c2", name="fetch")]),
        _chunk(tool_calls=[_tc(0, arguments='{"q":"x"}')]),
        _chunk(tool_calls=[_tc(1, arguments='{"url":"y"}')]),
    ]
    result = await stream_async(_aiter(chunks))
    assert len(result.tool_calls) == 2
    assert result.tool_calls[0]["function"]["name"] == "search"
    assert result.tool_calls[1]["function"]["name"] == "fetch"


@pytest.mark.asyncio
async def test_async_skips_empty_choices():
    chunks = [SimpleNamespace(choices=[]), _chunk(content="ok"), SimpleNamespace(choices=None)]
    result = await stream_async(_aiter(chunks))
    assert result.content == "ok"


@pytest.mark.asyncio
async def test_async_independent_results():
    """Each call returns a fresh StreamResult."""
    a = await stream_async(_aiter([_chunk(tool_calls=[_tc(0, tc_id="a", name="fa")])]))
    b = await stream_async(_aiter([_chunk(tool_calls=[_tc(0, tc_id="b", name="fb")])]))
    assert a.tool_calls[0]["id"] == "a"
    assert b.tool_calls[0]["id"] == "b"
    assert a.tool_calls is not b.tool_calls


# --- stream_sync ---


def test_sync_content_only(capsys: pytest.CaptureFixture[str]):
    result = stream_sync(iter([_chunk(content="Hello"), _chunk(content=" world")]))
    assert result.content == "Hello world"
    assert result.tool_calls == []
    assert "Hello world" in capsys.readouterr().out


def test_sync_empty():
    result = stream_sync(iter([]))
    assert result.content == ""
    assert result.tool_calls == []


def test_sync_reassembles_tool_call():
    chunks = [
        _chunk(tool_calls=[_tc(0, tc_id="call_abc", name="gmail_send")]),
        _chunk(tool_calls=[_tc(0, arguments='{"to": "a@b.com"}')]),
        _chunk(content="Sent.", finish_reason="stop"),
    ]
    result = stream_sync(iter(chunks))
    assert result.tool_calls[0]["function"] == {"name": "gmail_send", "arguments": '{"to": "a@b.com"}'}
    assert result.content == "Sent."


def test_sync_thought_signature():
    chunks = [_chunk(tool_calls=[_tc(0, tc_id="c", name="fn", thought_signature="sig")])]
    result = stream_sync(iter(chunks))
    assert result.tool_calls[0]["thought_signature"] == "sig"
