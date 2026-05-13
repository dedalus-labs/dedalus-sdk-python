"""Record agent runs to a JSON trace file.

Quick start::

    from dedalus_labs.lib.replay import Recorder

    with Recorder("trace.json") as rec:
        runner.run(
            model="openai/gpt-5-nano",
            input="...",
            tools=[add],
            on_tool_event=rec.on_tool,
            on_model_event=rec.on_model,
        )

The trace file is local-only. See ``docs/replay.md`` for the privacy model,
the trace format, and how to compose redactors.
"""

from ._events import (
    FORMAT_VERSION,
    MODEL_REQUEST,
    MODEL_RESPONSE,
    TOOL_END,
    build_envelope,
)
from ._recorder import Recorder
from ._redact import redact_api_keys, redact_bearer_tokens, redact_emails

__all__ = [
    "FORMAT_VERSION",
    "MODEL_REQUEST",
    "MODEL_RESPONSE",
    "TOOL_END",
    "Recorder",
    "build_envelope",
    "redact_api_keys",
    "redact_bearer_tokens",
    "redact_emails",
]
