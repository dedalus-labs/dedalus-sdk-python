from __future__ import annotations

import json
from typing import Any, Callable
from pathlib import Path

from ..runner import DedalusRunner
from ._events import FORMAT_VERSION
from ...types.chat import ChatCompletion
from ._fake_client import _FakeClient


class Replayer:
    """Re-run an agent conversation from a recorded trace.

    Reuses the production DedalusRunner end-to-end. Only the model client
    and local tool functions are replaced with recorded-data stubs — policy,
    message building, scheduling, and MCP composition all run as in
    production.

    Usage::

        result = Replayer.from_file("trace.json").run()
        print(result.final_output)

        # Substitute a fixed tool implementation
        result = Replayer.from_file("trace.json").run(
            swap_tool={"add": lambda a, b: a + b},
        )

        # Route through a real model instead
        from dedalus_labs import Dedalus
        result = Replayer.from_file("trace.json").run(
            swap_client=Dedalus(),
        )
    """

    def __init__(self, trace: dict[str, Any]) -> None:
        self._trace = trace
        self._validate()

    @classmethod
    def from_file(cls, path: str | Path) -> "Replayer":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    @classmethod
    def from_dict(cls, trace: dict[str, Any]) -> "Replayer":
        return cls(trace)

    def _validate(self) -> None:
        v = self._trace.get("format_version")
        if v != FORMAT_VERSION:
            raise ValueError(
                f"unsupported trace format_version={v!r} "
                f"(this Replayer reads {FORMAT_VERSION!r})"
            )
        if not isinstance(self._trace.get("events"), list):
            raise ValueError("trace is missing an `events` list")

    def run(
        self,
        *,
        swap_tool: dict[str, Callable[..., Any]] | None = None,
        swap_client: Any = None,
    ) -> Any:
        """Replay the recorded conversation.

        Parameters
        ----------
        swap_tool:
            Map of tool name -> callable. Named tools run your callable
            instead of the recorded stub. Useful for A/B-testing a fix.
        swap_client:
            A real Dedalus client. Routes model calls to the live API
            using the recorded messages and tools as context.
        """
        events = self._trace["events"]

        first_req = next(
            (e for e in events if e["kind"] == "model_request"), None
        )
        if first_req is None:
            raise ValueError("trace contains no model_request events")

        req = first_req["request"]

        responses = [
            ChatCompletion.model_validate(e["response"])
            for e in events
            if e["kind"] == "model_response"
        ]

        recorded_tool_ends: dict[str, list[dict[str, Any]]] = {}
        for e in events:
            if e["kind"] == "tool_end":
                recorded_tool_ends.setdefault(e["name"], []).append(e)

        # Union both sources so MCP-only tools (no tool_end events) are still surfaced
        tool_names = set(recorded_tool_ends) | {
            t["function"]["name"]
            for t in (req.get("tools") or [])
        }

        swap_tool = swap_tool or {}
        tools: list[Callable[..., Any]] = []
        for name in tool_names:
            if name in swap_tool:
                fn = swap_tool[name]
                if fn.__name__ != name:
                    # Runner dispatches by __name__; rename without mutating caller's fn
                    wrapped = lambda *a, _fn=fn, **kw: _fn(*a, **kw)
                    wrapped.__name__ = name
                    fn = wrapped
                tools.append(fn)
            else:
                tools.append(_make_replay_tool(name, recorded_tool_ends.get(name, [])))

        client = swap_client or _FakeClient(responses)
        runner = DedalusRunner(client)

        messages = req.get("messages") or []
        initial_input = messages[0]["content"] if messages else ""

        return runner.run(
            model=req["model"],
            input=initial_input,
            tools=tools or None,
            mcp_servers=req.get("mcp_servers") or None,
        )


# ---------------------------------------------------------------------------
# Helpers


def _make_replay_tool(name: str, recorded_calls: list[dict[str, Any]]) -> Callable[..., Any]:
    """Return a callable that pops the next recorded result for `name`."""
    queue = list(recorded_calls)

    def replay_fn(**kwargs: Any) -> Any:  # noqa: ARG001
        if not queue:
            raise RuntimeError(
                f"replay drift: model called tool {name!r} more times than "
                f"recorded. Pass swap_tool={{'{name}': <fn>}} to bridge."
            )
        ev = queue.pop(0)
        if ev.get("error"):
            raise RuntimeError(ev["error"])
        return ev["result"]

    replay_fn.__name__ = name
    return replay_fn
