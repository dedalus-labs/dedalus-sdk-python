"""Recorder: capture runner events to a JSON file."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Union, Callable, Optional
from pathlib import Path

from ._events import build_envelope
from ..._utils._json import _CustomEncoder

EventDict = Dict[str, Any]
RedactFn = Callable[[EventDict], EventDict]


class Recorder:
    """Capture runner events to a JSON file for later inspection or replay.

    Pass the bound methods ``on_tool`` and ``on_model`` as runner callbacks.
    Use the Recorder as a context manager so the file is written on exit::

        with Recorder("trace.json") as rec:
            runner.run(
                model="openai/gpt-5-nano",
                input="What is 3 + 4?",
                tools=[add],
                on_tool_event=rec.on_tool,
                on_model_event=rec.on_model,
            )

    The file lives only on local disk. Nothing is sent over the network.

    If ``redact`` is provided, it runs on every event before the event is
    stored in memory — raw values never live in the Recorder. The function
    should accept and return an event dict.

    ``metadata`` is embedded in the trace envelope verbatim. Use it for
    context like ticket IDs or customer IDs that aren't part of the agent
    interaction itself.
    """

    def __init__(
        self,
        path: Union[str, Path],
        *,
        redact: Optional[RedactFn] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._path = Path(path)
        self._redact = redact
        self._metadata = dict(metadata or {})
        self._events: List[EventDict] = []
        self._closed = False

    # -- runner callback targets --------------------------------------------

    def on_tool(self, event: EventDict) -> None:
        """Callback for ``runner.run(on_tool_event=...)``."""
        self._record(event)

    def on_model(self, event: EventDict) -> None:
        """Callback for ``runner.run(on_model_event=...)``."""
        self._record(event)

    # -- internals ----------------------------------------------------------

    def _record(self, event: EventDict) -> None:
        stamped: EventDict = {**event, "ts": time.time()}
        if self._redact is None:
            self._events.append(stamped)
            return
        try:
            self._events.append(self._redact(stamped))
        except Exception:
            # Redaction must never break the run. Mark the event so the
            # operator can spot redaction failures by reading the trace.
            self._events.append({**stamped, "_redaction_failed": True})

    # -- output -------------------------------------------------------------

    def save(self) -> None:
        """Write the trace JSON to disk. Idempotent."""
        if self._closed:
            return
        envelope = build_envelope(self._events, self._metadata)
        # Pretty-print so the trace file is readable by hand. Reuses the
        # SDK's custom encoder for datetime and Pydantic support.
        self._path.write_text(
            json.dumps(envelope, cls=_CustomEncoder, indent=2, ensure_ascii=False, allow_nan=False),
            encoding="utf-8",
        )
        self._closed = True

    @property
    def events(self) -> List[EventDict]:
        """Captured events (read-only view for inspection in tests)."""
        return list(self._events)

    # -- context manager ----------------------------------------------------

    def __enter__(self) -> "Recorder":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.save()
