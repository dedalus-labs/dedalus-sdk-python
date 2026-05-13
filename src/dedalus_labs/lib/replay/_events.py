"""Trace format constants and envelope construction.

The trace format is intentionally simple JSON. See ``docs/replay.md`` for the
full schema and the reasoning behind the choices.
"""

from __future__ import annotations

from typing import Any, Dict, List
from datetime import datetime, timezone

from ..._version import __version__

# Bump on backwards-incompatible trace format changes.
# Readers should reject unknown major versions; future minor/patch versions
# may add fields and remain forward-compatible.
FORMAT_VERSION = "1.0"

# Event kinds the runner emits. Constants exposed so callers can filter or
# assert on event types without stringly-typed comparisons.
MODEL_REQUEST = "model_request"
MODEL_RESPONSE = "model_response"
TOOL_END = "tool_end"


def build_envelope(events: List[Dict[str, Any]], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap a list of events in the v1 trace envelope.

    The envelope is the structure that lands in the trace JSON file. It
    carries enough metadata for a reader to know what SDK version produced
    the trace and when, plus any user-supplied context (ticket IDs, etc.).
    """
    return {
        "format_version": FORMAT_VERSION,
        "sdk_version": __version__,
        "recorded_at": _now_iso(),
        "metadata": dict(metadata),
        "events": list(events),
    }


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
