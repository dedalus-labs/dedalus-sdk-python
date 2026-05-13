"""Tests for `dedalus_labs.lib.replay.Replayer` and `_fake_client`."""

from __future__ import annotations

import pytest

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
