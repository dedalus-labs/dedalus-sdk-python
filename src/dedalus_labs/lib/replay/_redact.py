"""Default redactors for use with ``Recorder(redact=...)``.

Each redactor takes an event dict and returns a new event dict with matching
substrings replaced by ``[REDACTED]``. The original event is not mutated;
redactors walk dicts/lists/tuples recursively.

Compose redactors by chaining them in a small lambda::

    def redact(event):
        event = redact_emails(event)
        event = redact_bearer_tokens(event)
        return event

    with Recorder("trace.json", redact=redact) as rec:
        ...
"""

from __future__ import annotations

import re
from typing import Any, Callable

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_BEARER_RE = re.compile(r"\bBearer\s+[\w.\-+/=]+", re.IGNORECASE)
_API_KEY_RE = re.compile(r"\b(?:sk|dsk|pk|api)[-_][\w-]{10,}\b")

_PLACEHOLDER = "[REDACTED]"


def redact_emails(event: dict[str, Any]) -> dict[str, Any]:
    """Replace email-like substrings with ``[REDACTED]``."""
    return _walk(event, lambda s: _EMAIL_RE.sub(_PLACEHOLDER, s))


def redact_bearer_tokens(event: dict[str, Any]) -> dict[str, Any]:
    """Replace ``Bearer <token>`` substrings with ``Bearer [REDACTED]``."""
    return _walk(event, lambda s: _BEARER_RE.sub(f"Bearer {_PLACEHOLDER}", s))


def redact_api_keys(event: dict[str, Any]) -> dict[str, Any]:
    """Replace common API key shapes (``sk-...``, ``dsk-...``, ``pk-...``, ``api_...``)."""
    return _walk(event, lambda s: _API_KEY_RE.sub(_PLACEHOLDER, s))


def _walk(obj: Any, fn: Callable[[str], str]) -> Any:
    """Recursively apply ``fn`` to every string inside a JSON-ish structure."""
    if isinstance(obj, str):
        return fn(obj)
    if isinstance(obj, dict):
        return {k: _walk(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk(v, fn) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_walk(v, fn) for v in obj)
    return obj
