"""Record an agent run to trace.json.

Usage:
    DEDALUS_API_KEY=<key> python examples/replay/01_record.py

The script asks the model to add two numbers using a local Python tool.
After the run, open trace.json to see the full record: model requests,
model responses, and the tool call result.
"""

import json
import sys
from pathlib import Path

from dedalus_labs import Dedalus
from dedalus_labs.lib.runner import DedalusRunner
from dedalus_labs.lib.replay import Recorder


def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


def main() -> None:
    client = Dedalus()
    runner = DedalusRunner(client)
    trace_path = Path("trace.json")

    with Recorder(trace_path) as rec:
        result = runner.run(
            model="openai/gpt-5-nano",
            input="What is 3 + 4? You must call the add tool.",
            tools=[add],
            on_tool_event=rec.on_tool,
            on_model_event=rec.on_model,
        )

    print(f"Answer : {result.final_output}")
    print(f"Trace  : {trace_path} ({trace_path.stat().st_size} bytes)")

    trace = json.loads(trace_path.read_text())
    kinds = [e["kind"] for e in trace["events"]]
    print(f"Events : {kinds}")


if __name__ == "__main__":
    sys.exit(main())
