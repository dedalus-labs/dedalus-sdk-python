"""Record a multi-tool, multi-step, multi-model run.

Exercises:
  - Two local tools (`add`, `multiply`)
  - Multi-step reasoning where step 2 depends on step 1's result
  - Tool-use that requires recalling a training-time fact
    (the year GPT-5 came out)
  - A handoff prompt across two models (gpt-5-nano + claude-sonnet-4-5)

Usage:
    DEDALUS_API_KEY=<key> python examples/replay/03_multi_tool.py

After this writes trace_multi.json, replay it with:
    python examples/replay/02_replay.py trace_multi.json

Note on handoffs: passing model=[a, b] makes the server advertise a
`transfer_to_*` tool to the primary model, but client-side execution of
that handoff tool is not enabled by default in this SDK build. The model
may emit a `transfer_to_*` call that the runner does not resolve. The
recorder captures this faithfully — see how replay reproduces the exact
final state, even when the live run ended on an unresolved handoff.
"""

import json
import sys
from pathlib import Path

from dedalus_labs import Dedalus
from dedalus_labs.lib.replay import Recorder
from dedalus_labs.lib.runner import DedalusRunner


def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the product."""
    return a * b


PROMPT = (
    "Log all model handoffs you conduct. Use your tools to do this:\n"
    "1) Add 3 + 5.\n"
    "2) Multiply the result from step 1 by the year GPT-5 came out.\n"
    "3) Handoff to sonnet and write a poem about the number from step 2. "
    "Output the actual poem."
)


def main() -> None:
    client = Dedalus()
    runner = DedalusRunner(client)
    trace_path = Path("trace_multi.json")

    with Recorder(trace_path) as rec:
        result = runner.run(
            model=["openai/gpt-5-nano", "anthropic/claude-sonnet-4-5"],
            input=PROMPT,
            tools=[add, multiply],
            on_tool_event=rec.on_tool,
            on_model_event=rec.on_model,
        )

    print("=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result.final_output)
    print()
    print(f"Trace : {trace_path} ({trace_path.stat().st_size} bytes)")

    trace = json.loads(trace_path.read_text())
    kinds = [e["kind"] for e in trace["events"]]
    print(f"Events: {kinds}")
    print(f"Tools called: {[e['name'] for e in trace['events'] if e['kind'] == 'tool_end']}")


if __name__ == "__main__":
    sys.exit(main())
