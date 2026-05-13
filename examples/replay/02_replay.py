"""Replay an agent run from a recorded trace.

Usage:
    python examples/replay/02_replay.py [trace.json]

Reads the trace file, re-runs the conversation through DedalusRunner with
a fake client and synthetic tools, and prints the final answer. No network
calls are made.

First run examples/replay/01_record.py to produce trace.json.
"""

import sys
from pathlib import Path

from dedalus_labs.lib.replay import Replayer


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "trace.json")
    if not path.exists():
        print(f"Trace not found: {path}")
        print("Run examples/replay/01_record.py first to record a trace.")
        sys.exit(1)

    result = Replayer.from_file(path).run()

    print(f"Replayed from : {path}")
    print(f"Final output  : {result.final_output}")


if __name__ == "__main__":
    main()
