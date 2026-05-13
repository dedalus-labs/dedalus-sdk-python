# Record/replay — capture and inspect agent runs

`dedalus_labs.lib.replay` lets you save a complete record of any agent run to
a local JSON file. You can open that file, read what the agent did, and — in a
future release — replay the run deterministically for debugging.

---

## Privacy model

Recording is **opt-in** and **local-first**:

- Nothing is uploaded anywhere. The trace lands in a file on your machine.
- Recording only happens when you pass `on_tool_event=rec.on_tool` and
  `on_model_event=rec.on_model` to `runner.run()`. A run without those
  arguments produces no trace.
- What is captured: every model request payload (messages, tools, model name)
  and every model response (including raw tool calls), plus each tool
  result (name, arguments, return value).
- What is **not** captured: anything the runner never sees — secrets already
  in environment variables, TLS-layer bytes, MCP-server internals.

If trace files will leave your machine (shared with a customer, attached to an
issue), use the built-in redactors before saving:

```python
from dedalus_labs.lib.replay import Recorder, redact_emails, redact_bearer_tokens

def redact(event):
    event = redact_emails(event)
    event = redact_bearer_tokens(event)
    return event

with Recorder("trace.json", redact=redact) as rec:
    runner.run(..., on_tool_event=rec.on_tool, on_model_event=rec.on_model)
```

---

## Quick start

```python
from dedalus_labs import Dedalus
from dedalus_labs.lib.runner import DedalusRunner
from dedalus_labs.lib.replay import Recorder

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

client = Dedalus()
runner = DedalusRunner(client)

with Recorder("trace.json") as rec:
    result = runner.run(
        model="openai/gpt-5-nano",
        input="What is 3 + 4? Use the add tool.",
        tools=[add],
        on_tool_event=rec.on_tool,
        on_model_event=rec.on_model,
    )

print(result.final_output)
# trace.json now contains the full run
```

---

## Recorder API

```python
Recorder(path, *, redact=None, metadata=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `str \| Path` | Where to write the trace file. |
| `redact` | `Callable[[dict], dict] \| None` | Called on each event before it is stored. Return a modified copy; raise to fall back to marking the event `_redaction_failed`. |
| `metadata` | `dict \| None` | Arbitrary key-value pairs written into the trace envelope (ticket IDs, customer names, environment tags, etc.). |

**Methods:**

- `rec.on_tool(event)` — pass as `on_tool_event=` in `runner.run()`.
- `rec.on_model(event)` — pass as `on_model_event=` in `runner.run()`.
- `rec.save()` — write the file immediately. Called automatically on `__exit__`.

Use as a context manager (`with Recorder(...) as rec`) — `save()` is called
even if the run raises.

---

## Trace format (v1.0)

The file is UTF-8 JSON, pretty-printed with two-space indentation.

```json
{
  "format_version": "1.0",
  "sdk_version": "0.3.0",
  "recorded_at": "2026-05-12T15:02:11Z",
  "metadata": {},
  "events": [
    {
      "kind": "model_request",
      "step": 1,
      "request": { "model": "openai/gpt-5-nano", "messages": [...], "tools": [...] },
      "ts": 1715526131.04
    },
    {
      "kind": "model_response",
      "step": 1,
      "response": { "id": "chatcmpl-...", "choices": [...] },
      "ts": 1715526132.41
    },
    {
      "kind": "tool_end",
      "step": 1,
      "name": "add",
      "tool_call_id": "call_abc123",
      "arguments": "{\"a\": 3, \"b\": 4}",
      "result": 7,
      "ts": 1715526132.63
    },
    {
      "kind": "model_request",
      "step": 2,
      "request": { ... },
      "ts": 1715526132.71
    },
    {
      "kind": "model_response",
      "step": 2,
      "response": { ... },
      "ts": 1715526133.92
    }
  ]
}
```

### Envelope fields

| Field | Description |
|-------|-------------|
| `format_version` | Schema version. Bump on breaking changes. |
| `sdk_version` | `dedalus_labs.__version__` at record time. |
| `recorded_at` | UTC ISO-8601 timestamp when `save()` was called. |
| `metadata` | User-supplied dict (pass via `Recorder(..., metadata={...})`). |
| `events` | Ordered list of event objects. |

### Event fields (all events)

| Field | Description |
|-------|-------------|
| `kind` | `"model_request"`, `"model_response"`, or `"tool_end"`. |
| `step` | Turn counter from the runner (starts at 1). |
| `ts` | Unix timestamp (float) when the event was recorded. |

### `model_request` extra fields

| Field | Description |
|-------|-------------|
| `request` | The kwargs passed to `client.chat.completions.create`, serialized. |

### `model_response` extra fields

| Field | Description |
|-------|-------------|
| `response` | The `ChatCompletion` object serialized via `model_dump(mode="json")`. |

### `tool_end` extra fields

| Field | Description |
|-------|-------------|
| `name` | Tool function name. |
| `tool_call_id` | ID from the model's tool call request. |
| `arguments` | Raw JSON string of arguments the model passed. |
| `result` | Return value of the tool function. |
| `error` | Present only if the tool raised; contains the error message string. |

---

## Built-in redactors

```python
from dedalus_labs.lib.replay import redact_emails, redact_bearer_tokens, redact_api_keys
```

Each redactor walks the event dict recursively and replaces matching strings:

| Redactor | Pattern replaced | Replacement |
|----------|-----------------|-------------|
| `redact_emails` | `user@example.com` style | `[REDACTED_EMAIL]` |
| `redact_bearer_tokens` | `Bearer <token>` in any string value | `Bearer [REDACTED]` |
| `redact_api_keys` | `sk-...`, `dsk-...`, `key-...` patterns | `[REDACTED_KEY]` |

Compose them:

```python
def redact(event):
    event = redact_emails(event)
    event = redact_bearer_tokens(event)
    event = redact_api_keys(event)
    return event
```

---

## Replaying a trace

`Replayer` reads a `trace.json` and re-runs the recorded conversation
through the production `DedalusRunner` - no API calls, no MCP traffic.

```python
from dedalus_labs.lib.replay import Replayer

result = Replayer.from_file("trace.json").run()
print(result.final_output)
```

Internally, `Replayer` injects a fake client whose `chat.completions.create()`
serves the recorded `ChatCompletion` objects in order, and substitutes each
local tool with a stub that returns the recorded result. The runner walks
its normal step loop; nothing is mocked except the two outward seams.

### `Replayer.run(...)` parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `swap_tool` | `dict[str, Callable] \| None` | Map of tool name to callable. Named tools run your function instead of the recorded stub. Useful for A/B-testing a fix. |
| `swap_client` | `Dedalus \| None` | A live client. Routes model calls to the real API using the recorded messages and tools as context. |

```python
# A/B-test a tool fix against the same recorded conversation
def better_add(a: int, b: int) -> int:
    return a + b

Replayer.from_file("trace.json").run(swap_tool={"add": better_add})

# Run the recorded conversation against a real model
from dedalus_labs import Dedalus
Replayer.from_file("trace.json").run(swap_client=Dedalus())
```

### Drift detection

Replay fails loudly when the recorded behavior and current code paths
diverge:

- **More model calls than recorded** - the fake client raises a `RuntimeError`
  pointing at `swap_client=` as the bridge.
- **More tool calls for a name than recorded** - the synthetic tool raises
  pointing at `swap_tool={name: ...}`.
- **Unknown `format_version`** - `from_file` / `from_dict` raises `ValueError`
  during construction.

A drift error usually means the customer's recorded run hits a code path
that no longer exists locally. That is exactly the bug an FDE wants to
surface, not silently swallow.

---

## Out of scope (follow-up issues)

The following are intentional non-goals for v1. File a new issue if you need one:

- **Streaming recording / replay** — `_execute_streaming_*` paths are not instrumented.
- **Per-tool start events** — `tool_start` events with timing inside parallel batches.
- **Cloud upload / hosted viewer** — traces are local-only.
- **OpenTelemetry export** — the event format is not OTel-compatible today.
- **Trace diffing** — comparing two trace files for regression testing.
- **Schema migration** — tooling to upgrade `format_version` 1.0 traces to future versions.
