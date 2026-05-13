from __future__ import annotations

from typing import Any

from ...types.chat import ChatCompletion


class _FakeCompletions:
    def __init__(self, responses: list[ChatCompletion]) -> None:
        self._queue = list(responses)

    def create(self, **kwargs: Any) -> ChatCompletion:  # noqa: ARG002
        if not self._queue:
            raise RuntimeError(
                "replay drift: runner requested more model responses than the trace "
                "recorded. Pass swap_client=Dedalus() to continue with a real model."
            )
        return self._queue.pop(0)


class _FakeChat:
    def __init__(self, responses: list[ChatCompletion]) -> None:
        self.completions = _FakeCompletions(responses)


class _FakeClient:
    """Minimal client shim that serves recorded ChatCompletion objects.

    Not an instance of AsyncDedalus, so DedalusRunner routes to the sync
    execution path (_execute_turns_sync).
    """

    def __init__(self, responses: list[ChatCompletion]) -> None:
        self.chat = _FakeChat(responses)
