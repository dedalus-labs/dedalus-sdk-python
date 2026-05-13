# Replay examples

| Script | What it shows |
|--------|---------------|
| `01_record.py` | Record a tool-calling agent run to `trace.json` |
| `02_replay.py` | Re-run the recorded conversation locally with no API calls |

Run them in order:

```bash
DEDALUS_API_KEY=<key> python examples/replay/01_record.py
python examples/replay/02_replay.py trace.json
```

See [`docs/replay.md`](../../docs/replay.md) for the full API reference,
trace format, and privacy model.
