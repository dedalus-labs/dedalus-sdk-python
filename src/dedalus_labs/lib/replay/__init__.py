"""Record and replay agent runs via a local JSON trace file.

Record::

    from dedalus_labs.lib.replay import Recorder

    with Recorder("trace.json") as rec:
        runner.run(
            model="openai/gpt-5-nano",
            input="...",
            tools=[add],
            on_tool_event=rec.on_tool,
            on_model_event=rec.on_model,
        )

Replay::

    from dedalus_labs.lib.replay import Replayer

    result = Replayer.from_file("trace.json").run()

The trace file is local-only. See ``docs/replay.md`` for the privacy model,
the trace format, and how to compose redactors.
"""

from ._events import (
    TOOL_END,
    MODEL_REQUEST,
    FORMAT_VERSION,
    MODEL_RESPONSE,
    build_envelope,
)
from ._redact import redact_emails, redact_api_keys, redact_bearer_tokens
from ._recorder import Recorder
from ._replayer import Replayer

__all__ = [
    "FORMAT_VERSION",
    "MODEL_REQUEST",
    "MODEL_RESPONSE",
    "TOOL_END",
    "Recorder",
    "Replayer",
    "build_envelope",
    "redact_api_keys",
    "redact_bearer_tokens",
    "redact_emails",
]
