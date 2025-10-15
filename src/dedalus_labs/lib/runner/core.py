# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import copy
import json
import asyncio
import inspect
from typing import TYPE_CHECKING, Any, Dict, Callable, Iterable, Iterator, Protocol, Sequence, Union
from dataclasses import field, dataclass

from dedalus_labs import Dedalus, AsyncDedalus

if TYPE_CHECKING:  # pragma: no cover - optional runtime dependency
    from ...types.dedalus_model import DedalusModel

from .types import Message, ToolCall, JsonValue, ToolResult
from ..utils import to_schema
from .guardrails import GuardrailCheckResult, GuardrailFunc, InputGuardrailTriggered, OutputGuardrailTriggered


@dataclass
class RunnerHooks:
    on_before_run: Callable[[list[Message]], None] | None = None
    on_after_run: Callable[["_RunResult"], None] | None = None
    on_before_model_call: Callable[[dict[str, Any]], None] | None = None
    on_after_model_call: Callable[[Any], None] | None = None
    on_before_tool: Callable[[str, Dict[str, Any]], None] | None = None
    on_after_tool: Callable[[str, JsonValue | Exception], None] | None = None
    on_guardrail_trigger: Callable[[str, GuardrailCheckResult], None] | None = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _render_model_spec(spec: str | Sequence[str]) -> str:
    if isinstance(spec, (list, tuple)):
        return ", ".join(str(item) for item in spec)
    return str(spec)


def _truncate(value: str, length: int = 80) -> str:
    if len(value) <= length:
        return value
    return value[: length - 1] + "…"


def _jsonify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except TypeError:
        return str(value)

def _parse_arguments(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if not raw:
        return {}
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return {}


def _message_to_dict(message: Any) -> Dict[str, Any]:
    if hasattr(message, "model_dump"):
        try:
            return message.model_dump()
        except Exception:  # pragma: no cover - defensive guard
            pass
    if hasattr(message, "dict"):
        try:
            return message.dict()
        except Exception:  # pragma: no cover
            pass
    if hasattr(message, "__dict__"):
        return {k: v for k, v in vars(message).items() if not k.startswith("_")}
    if isinstance(message, dict):
        return dict(message)
    return {}


# ---------------------------------------------------------------------------
# Logging utilities
# ---------------------------------------------------------------------------


@dataclass
class _DebugLogger:
    enabled: bool
    debug: bool

    def log(self, message: str) -> None:
        if self.enabled:
            print(f"[DedalusRunner] {message}")  # noqa: T201

    def step(self, step: int, max_steps: int) -> None:
        self.log(f"Step {step}/{max_steps}")

    def models(self, requested: str | Sequence[str], previous: str | Sequence[str] | None) -> None:
        if not self.enabled:
            return
        current = _render_model_spec(requested)
        if previous is None:
            self.log(f"Calling model: {current}")
        else:
            prev = _render_model_spec(previous)
            if prev != current:
                self.log(f"Handoff to model: {current}")

    def tool_schema(self, tool_names: list[str]) -> None:
        if self.enabled and tool_names:
            self.log(f"Local tools available: {tool_names}")

    def tool_execution(self, name: str, result: Any, *, error: bool = False) -> None:
        if not self.enabled:
            return
        summary = _truncate(_jsonify(result))
        verb = "errored" if error else "returned"
        self.log(f"Tool {name} {verb}: {summary}")

    def messages_snapshot(self, messages: list[Message]) -> None:
        if not (self.enabled and self.debug):
            return
        self.log("Conversation so far:")
        for idx, msg in enumerate(messages[-6:]):
            role = msg.get("role", "?")
            content = msg.get("content")
            if isinstance(content, list):
                snippet = "[array content]"
            else:
                snippet = _truncate(_jsonify(content or ""), 60)
            self.log(f"  [{idx}] {role}: {snippet}")

    def final_summary(self, models: list[str], tools: list[str]) -> None:
        if not self.enabled:
            return
        self.log(f"Models used: {models}")
        self.log(f"Tools called: {tools}")


# ---------------------------------------------------------------------------
# Tool handling
# ---------------------------------------------------------------------------

class _FunctionToolHandler:
    def __init__(self, funcs: Iterable[Callable[..., Any]]):
        self._funcs = {fn.__name__: fn for fn in funcs}

    def schemas(self) -> list[Dict[str, Any]]:
        out: list[Dict[str, Any]] = []
        for fn in self._funcs.values():
            try:
                out.append(to_schema(fn))
            except Exception:  # pragma: no cover - best effort schema extraction
                continue
        return out

    def exec_sync(self, name: str, args: Dict[str, JsonValue]) -> JsonValue:
        fn = self._funcs[name]
        if inspect.iscoroutinefunction(fn):
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(fn(**args))
            finally:  # pragma: no cover - cleanup path
                loop.close()
        return fn(**args)


# ---------------------------------------------------------------------------
# Runner state
# ---------------------------------------------------------------------------


@dataclass
class _RunnerState:
    model: str | list[str]
    request_kwargs: Dict[str, Any]
    auto_execute_tools: bool
    max_steps: int
    mcp_servers: list[str]
    logger: _DebugLogger
    tool_handler: _FunctionToolHandler
    input_guardrails: list[GuardrailFunc]
    output_guardrails: list[GuardrailFunc]
    hooks: RunnerHooks
    stream: bool

@dataclass
class _RunResult:
    final_output: str
    tool_results: list[ToolResult]
    steps_used: int
    messages: list[Message] = field(default_factory=list)
    tools_called: list[str] = field(default_factory=list)
    models_used: list[str] = field(default_factory=list)
    input_guardrail_results: list[GuardrailCheckResult] = field(default_factory=list)
    output_guardrail_results: list[GuardrailCheckResult] = field(default_factory=list)

    @property
    def output(self) -> str:  # backwards compatibility
        return self.final_output

    @property
    def content(self) -> str:  # backwards compatibility
        return self.final_output

    def to_input_list(self) -> list[Message]:
        return list(self.messages)


# ---------------------------------------------------------------------------
# DedalusRunner (lean version)
# ---------------------------------------------------------------------------


class DedalusRunner:
    """Minimal higher-level helper around the Chat Completions API."""

    def __init__(self, client: Dedalus | AsyncDedalus, *, verbose: bool = False):
        self.client = client
        self.verbose = verbose

    def run(
        self,
        input: str | list[Message] | None = None,
        tools: Iterable[Callable[..., Any]] | None = None,
        messages: list[Message] | None = None,
        instructions: str | None = None,
        model: str | list[str] | "DedalusModel" | Iterable["DedalusModel"] | None = None,
        max_steps: int = 10,
        mcp_servers: Iterable[str] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        logit_bias: Dict[str, int] | None = None,
        stream: bool = False,
        transport: str = "http",
        auto_execute_tools: bool = True,
        verbose: bool | None = None,
        debug: bool | None = None,
        on_tool_event: Callable[[Dict[str, JsonValue]], None] | None = None,  # legacy, unused
        return_intent: bool = False,
        agent_attributes: Dict[str, float] | None = None,
        model_attributes: Dict[str, Dict[str, float]] | None = None,
        tool_choice: str | Dict[str, JsonValue] | None = None,
        guardrails: list[Dict[str, JsonValue]] | None = None,
        handoff_config: Dict[str, JsonValue] | None = None,
        input_guardrails: Iterable[GuardrailFunc] | None = None,
        output_guardrails: Iterable[GuardrailFunc] | None = None,
        hooks: RunnerHooks | None = None,
        _available_models: Iterable[str] | None = None,  # legacy, ignored
        _strict_models: bool = True,  # legacy, ignored
    ) -> Union[_RunResult, Iterator[Any]]:
        """Run the assistant until completion or tool-call deferral.

        When stream=True, returns an Iterator that yields chunks and can be passed to stream_sync().
        When stream=False, returns a _RunResult with the final output.
        """

        if model is None:
            raise ValueError("model must be provided")

        # Streaming is supported - when enabled, the runner will stream responses in real-time
        # Note: Requires server-side SSE (Server-Sent Events) support
        # If streaming fails with JSON decode errors, the server may not support SSE format

        if transport != "http":
            raise ValueError("DedalusRunner currently supports only HTTP transport")

        if return_intent:
            import warnings

            warnings.warn(
                "`return_intent` is deprecated; use auto_execute_tools=False to inspect raw tool_calls.",
                UserWarning,
                stacklevel=2,
            )

        if isinstance(self.client, AsyncDedalus):
            raise RuntimeError("DedalusRunner.run currently supports synchronous Dedalus clients only.")

        tool_handler = _FunctionToolHandler(list(tools or []))
        logger = _DebugLogger(enabled=self.verbose if verbose is None else bool(verbose), debug=bool(debug))
        logger.tool_schema(list(tool_handler._funcs.keys()))
        hook_state = hooks or RunnerHooks()

        model_spec = self._normalize_model_spec(model)
        request_kwargs = self._build_request_kwargs(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logit_bias=logit_bias,
            agent_attributes=agent_attributes,
            model_attributes=model_attributes,
            tool_choice=tool_choice,
            guardrails=guardrails,
            handoff_config=handoff_config,
        )

        state = _RunnerState(
            model=model_spec,
            request_kwargs=request_kwargs,
            auto_execute_tools=auto_execute_tools,
            max_steps=max(1, max_steps),
            mcp_servers=list(mcp_servers or []),
            logger=logger,
            tool_handler=tool_handler,
            input_guardrails=list(input_guardrails or []),
            output_guardrails=list(output_guardrails or []),
            hooks=hook_state,
            stream=stream,
        )

        conversation = self._initial_messages(instructions=instructions, input=input, messages=messages)
        self._call_hook(state.hooks.on_before_run, copy.deepcopy(conversation))
        input_guardrail_results = self._run_input_guardrails(conversation, state)

        # Branch to streaming or non-streaming implementation
        if stream:
            return self._run_streaming(conversation, state, input_guardrail_results)

        result = self._run_turns(conversation, state, input_guardrail_results)

        if on_tool_event is not None:
            # Preserve legacy callback behaviour for callers that still pass it.
            for tr in result.tool_results:
                try:  # pragma: no cover - optional behaviour
                    on_tool_event({"name": tr.get("name"), "result": tr.get("result"), "step": tr.get("step")})
                except Exception:
                    pass

        self._call_hook(state.hooks.on_after_run, result)
        return result

    # ------------------------------------------------------------------
    # Core loop
    # ------------------------------------------------------------------

    def _call_hook(self, hook: Callable[..., None] | None, *args: Any) -> None:
        if hook is None:
            return
        hook(*args)

    def _run_turns(
        self,
        conversation: list[Message],
        state: _RunnerState,
        input_guardrail_results: list[GuardrailCheckResult],
    ) -> _RunResult:
        history = list(conversation)
        tool_schemas = state.tool_handler.schemas() or None
        final_text = ""
        tool_results: list[ToolResult] = []
        tools_called: list[str] = []
        models_used: list[str] = []
        input_results = list(input_guardrail_results)
        output_results: list[GuardrailCheckResult] = []
        previous_model: str | Sequence[str] | None = None
        steps = 0

        while steps < state.max_steps:
            steps += 1
            state.logger.step(steps, state.max_steps)
            state.logger.messages_snapshot(history)

            state.logger.models(state.model, previous_model)

            self._call_hook(
                state.hooks.on_before_model_call,
                {
                    "model": state.model,
                    "messages": history,
                    "kwargs": state.request_kwargs,
                },
            )
            # DEBUG: Log MCP servers before sending to client
            print(f"[RUNNER DEBUG] state.mcp_servers = {state.mcp_servers}, type = {type(state.mcp_servers)}")
            print(f"[RUNNER DEBUG] state.mcp_servers or None = {state.mcp_servers or None}")

            # DEBUG: Log the actual parameters being passed
            create_params = {
                "model": state.model,
                "messages": history,
                "tools": tool_schemas,
                "mcp_servers": state.mcp_servers or None,
                "stream": state.stream,  # Use stream setting from state
                **state.request_kwargs,
            }
            print(f"[RUNNER DEBUG] Full create() params keys: {list(create_params.keys())}")
            print(f"[RUNNER DEBUG] mcp_servers param value: {create_params.get('mcp_servers')}")

            response = self.client.chat.completions.create(**create_params)

            # Handle streaming response
            if state.stream:
                # Collect chunks (no printing - user should use stream_async/stream_sync)
                collected_tool_calls: list[Dict[str, Any]] = []
                collected_content = []

                for chunk in response:
                    if chunk.choices:
                        choice = chunk.choices[0]
                        delta = getattr(choice, "delta", None)
                        if delta:
                            # Check for tool calls in delta
                            tool_calls_delta = getattr(delta, "tool_calls", None)
                            if tool_calls_delta:
                                self._accumulate_tool_calls(tool_calls_delta, collected_tool_calls)

                            # Check for content
                            content_piece = getattr(delta, "content", None)
                            if content_piece:
                                collected_content.append(content_piece)

                # Reconstruct response data from collected chunks
                if collected_tool_calls:
                    # Categorize tools into local vs MCP
                    local_tool_names = set(state.tool_handler._funcs.keys())
                    mcp_names = [
                        tc["function"]["name"] for tc in collected_tool_calls
                        if tc["function"]["name"] not in local_tool_names
                    ]
                    has_streamed_content = len(collected_content) > 0

                    # If MCP tools were called AND content was streamed, server handled it - we're done
                    if mcp_names and has_streamed_content:
                        final_text = "".join(collected_content)
                        if final_text:
                            history.append({"role": "assistant", "content": final_text})
                        break

                    # Check if ALL tools are MCP (none are local)
                    all_mcp = all(
                        tc["function"]["name"] not in local_tool_names
                        for tc in collected_tool_calls
                    )

                    if all_mcp:
                        # All tools are MCP - continue loop to get server's response
                        tool_calls = []
                    else:
                        # We have at least one local tool - filter and process only local tools
                        tool_calls = [
                            tc for tc in collected_tool_calls
                            if tc["function"]["name"] in local_tool_names
                        ]
                else:
                    # Final text response - no tool calls
                    tool_calls = []
                    final_text = "".join(collected_content)
                    if final_text:
                        history.append({"role": "assistant", "content": final_text})
                    break
            else:
                # Non-streaming response
                self._call_hook(state.hooks.on_after_model_call, response)

                if not getattr(response, "choices", None):
                    break

                choice = response.choices[0]
                message_dict = _message_to_dict(choice.message)
                tool_calls = message_dict.get("tool_calls") or []
                content = message_dict.get("content")

                # No tool calls - this is the final response
                if not tool_calls:
                    final_text = content or ""
                    if final_text:
                        history.append({"role": "assistant", "content": final_text})
                    break

            models_used.append(_render_model_spec(state.model))
            previous_model = state.model

            tool_payloads = [self._coerce_tool_call(tc) for tc in tool_calls]
            for name in (payload["function"].get("name") for payload in tool_payloads):
                if name and name not in tools_called:
                    tools_called.append(name)

            history.append({"role": "assistant", "tool_calls": tool_payloads})

            if not state.auto_execute_tools:
                break

            self._execute_tool_calls_sync(
                tool_payloads,
                state.tool_handler,
                history,
                tool_results,
                tools_called,
                steps,
                state.logger,
                state.hooks,
            )

        if final_text:
            output_results = self._run_output_guardrails(final_text, state)

        state.logger.final_summary(models_used, tools_called)
        return _RunResult(
            final_output=final_text,
            tool_results=tool_results,
            steps_used=steps,
            messages=history,
            tools_called=tools_called,
            models_used=models_used,
            input_guardrail_results=input_results,
            output_guardrail_results=output_results,
        )

    def _run_streaming(
        self,
        conversation: list[Message],
        state: _RunnerState,
        input_guardrail_results: list[GuardrailCheckResult],
    ) -> Iterator[Any]:
        """Execute conversation with streaming - yields chunks while processing tool calls."""
        history = list(conversation)
        tool_schemas = state.tool_handler.schemas() or None
        previous_model: str | Sequence[str] | None = None
        steps = 0

        while steps < state.max_steps:
            steps += 1
            state.logger.step(steps, state.max_steps)
            state.logger.messages_snapshot(history)
            state.logger.models(state.model, previous_model)

            self._call_hook(
                state.hooks.on_before_model_call,
                {
                    "model": state.model,
                    "messages": history,
                    "kwargs": state.request_kwargs,
                },
            )

            # DEBUG: Log MCP servers before sending to client
            print(f"[RUNNER DEBUG] state.mcp_servers = {state.mcp_servers}, type = {type(state.mcp_servers)}")
            print(f"[RUNNER DEBUG] state.mcp_servers or None = {state.mcp_servers or None}")

            create_params = {
                "model": state.model,
                "messages": history,
                "tools": tool_schemas,
                "mcp_servers": state.mcp_servers or None,
                "stream": True,  # Always stream
                **state.request_kwargs,
            }
            print(f"[RUNNER DEBUG] Full create() params keys: {list(create_params.keys())}")
            print(f"[RUNNER DEBUG] mcp_servers param value: {create_params.get('mcp_servers')}")

            stream = self.client.chat.completions.create(**create_params)

            # Yield chunks while accumulating tool calls and content
            collected_tool_calls: list[Dict[str, Any]] = []
            collected_content: list[str] = []

            chunk_count = 0
            for chunk in stream:
                chunk_count += 1
                if chunk.choices:
                    choice = chunk.choices[0]
                    delta = getattr(choice, "delta", None)
                    if delta:
                        # Check for tool calls in delta
                        tool_calls_delta = getattr(delta, "tool_calls", None)
                        if tool_calls_delta:
                            self._accumulate_tool_calls(tool_calls_delta, collected_tool_calls)

                        # Check for content
                        content_piece = getattr(delta, "content", None)
                        if content_piece:
                            collected_content.append(content_piece)

                # Yield the chunk to the user
                yield chunk

            print(f"[STREAMING DEBUG] Total chunks: {chunk_count}, Content chunks: {len(collected_content)}, Tool calls: {len(collected_tool_calls)}")
            if collected_tool_calls:
                print(f"[STREAMING DEBUG] Tool calls collected:")
                for tc in collected_tool_calls:
                    print(f"  - {tc['function']['name']}: {tc['function']['arguments'][:100]}")

            # Process accumulated data after stream ends
            if collected_tool_calls:
                # Categorize tools into local vs MCP
                local_tool_names = set(state.tool_handler._funcs.keys())
                print(f"[STREAMING DEBUG] Local tool names: {local_tool_names}")
                mcp_names = [
                    tc["function"]["name"] for tc in collected_tool_calls
                    if tc["function"]["name"] not in local_tool_names
                ]
                print(f"[STREAMING DEBUG] MCP tool names: {mcp_names}")
                has_streamed_content = len(collected_content) > 0
                print(f"[STREAMING DEBUG] Has streamed content: {has_streamed_content}")

                # If MCP tools were called AND content was streamed
                # Check if there are also local tools to execute
                num_local = len(collected_tool_calls) - len(mcp_names)

                if mcp_names and has_streamed_content:
                    if num_local > 0:
                        # Server streamed content but there are also local tool calls
                        # Add the content to history first, then execute local tools
                        print(f"[STREAMING DEBUG] MCP + content + {num_local} local tools → adding content, executing locals")
                        final_text = "".join(collected_content)
                        if final_text:
                            history.append({"role": "assistant", "content": final_text})
                        # Fall through to execute local tools below
                    else:
                        # Only MCP tools and content - server handled everything
                        print(f"[STREAMING DEBUG] MCP + content (no locals) → breaking")
                        final_text = "".join(collected_content)
                        if final_text:
                            history.append({"role": "assistant", "content": final_text})
                        break

                # Local-first pattern: Filter to ONLY local tool calls when mixed
                # This executes local tools first, ignores MCP - model will call MCP next turn

                # Check if ALL tools are MCP (none are local)
                all_mcp = all(
                    tc["function"]["name"] not in local_tool_names
                    for tc in collected_tool_calls
                )

                if all_mcp:
                    # All MCP tools - don't add anything to history, continue
                    # Server will handle them on next iteration
                    print(f"[STREAMING DEBUG] All MCP tools ({len(mcp_names)}) - continuing for server execution")
                    continue

                # We have at least one local tool
                # Filter to ONLY include local tool calls (ignore MCP calls)
                local_only_tool_calls = [
                    tc for tc in collected_tool_calls
                    if tc["function"]["name"] in local_tool_names
                ]

                has_mixed = num_local > 0 and len(mcp_names) > 0
                if has_mixed:
                    print(f"[STREAMING DEBUG] Mixed tools: executing {len(local_only_tool_calls)} local, ignoring {len(mcp_names)} MCP")
                else:
                    print(f"[STREAMING DEBUG] Only local tools: executing {len(local_only_tool_calls)} local")

                # Add ONLY local tool calls to history
                local_payloads = [self._coerce_tool_call(tc) for tc in local_only_tool_calls]
                history.append({"role": "assistant", "tool_calls": local_payloads})

                if not state.auto_execute_tools:
                    break

                # Execute ONLY local tools
                for tc in local_only_tool_calls:
                    name = tc["function"].get("name", "")
                    args = _parse_arguments(tc["function"].get("arguments"))

                    self._call_hook(state.hooks.on_before_tool, name, args)
                    try:
                        result = state.tool_handler.exec_sync(name, args)
                        history.append({
                            "role": "tool",
                            "tool_call_id": tc.get("id", ""),
                            "content": _jsonify(result),
                        })
                        state.logger.tool_execution(name, result)
                        self._call_hook(state.hooks.on_after_tool, name, result)
                    except Exception as error:
                        history.append({
                            "role": "tool",
                            "tool_call_id": tc.get("id", ""),
                            "content": f"Error: {error}",
                        })
                        state.logger.tool_execution(name, error, error=True)
                        self._call_hook(state.hooks.on_after_tool, name, error)

                # Continue loop - if MCP tools were ignored, model will call them next turn
            else:
                # Final text response - no tool calls, we're done
                break

            previous_model = state.model

    # ------------------------------------------------------------------
    # Guardrail helpers
    # ------------------------------------------------------------------

    def _run_input_guardrails(
        self,
        conversation: list[Message],
        state: _RunnerState,
    ) -> list[GuardrailCheckResult]:
        if not state.input_guardrails:
            return []

        snapshot = copy.deepcopy(conversation)
        results: list[GuardrailCheckResult] = []
        for guardrail in state.input_guardrails:
            result = self._invoke_guardrail(guardrail, snapshot)
            if result.tripwire_triggered:
                state.logger.log(f"Input guardrail triggered: {self._guardrail_name(guardrail)}")
                self._call_hook(state.hooks.on_guardrail_trigger, self._guardrail_name(guardrail), result)
                raise InputGuardrailTriggered(result)
            results.append(result)
        return results

    def _run_output_guardrails(self, final_output: str, state: _RunnerState) -> list[GuardrailCheckResult]:
        if not state.output_guardrails:
            return []
        results: list[GuardrailCheckResult] = []
        for guardrail in state.output_guardrails:
            result = self._invoke_guardrail(guardrail, final_output)
            if result.tripwire_triggered:
                state.logger.log(f"Output guardrail triggered: {self._guardrail_name(guardrail)}")
                self._call_hook(state.hooks.on_guardrail_trigger, self._guardrail_name(guardrail), result)
                raise OutputGuardrailTriggered(result)
            results.append(result)
        return results

    def _invoke_guardrail(self, guardrail: GuardrailFunc, payload: Any) -> GuardrailCheckResult:
        try:
            outcome = guardrail(payload)
        except Exception as error:  # pragma: no cover - user code
            raise RuntimeError(f"Guardrail {self._guardrail_name(guardrail)} raised an exception") from error

        if inspect.isawaitable(outcome):
            outcome = asyncio.run(outcome)

        if isinstance(outcome, GuardrailCheckResult):
            return outcome

        if isinstance(outcome, dict) and "tripwire_triggered" in outcome:
            return GuardrailCheckResult(bool(outcome["tripwire_triggered"]), outcome.get("info"))

        if isinstance(outcome, tuple) and outcome:
            triggered = bool(outcome[0])
            info = outcome[1] if len(outcome) > 1 else None
            return GuardrailCheckResult(triggered, info)

        if outcome is None:
            return GuardrailCheckResult(False, None)

        return GuardrailCheckResult(bool(outcome), None)

    def _guardrail_name(self, guardrail: GuardrailFunc) -> str:
        return getattr(guardrail, "_guardrail_name", getattr(guardrail, "__name__", guardrail.__class__.__name__))

    def _initial_messages(
        self,
        instructions: str | None,
        input: str | list[Message] | None,
        messages: list[Message] | None,
    ) -> list[Message]:
        if instructions and messages:
            has_system = any(msg.get("role") == "system" for msg in messages)
            if has_system:
                raise ValueError("Cannot supply both 'instructions' and a system message in 'messages'.")

        if messages is not None:
            conversation = list(messages)
        elif input is not None:
            if isinstance(input, str):
                conversation = [{"role": "user", "content": input}]
            else:
                conversation = list(input)
        else:
            conversation = []

        if instructions:
            conversation.insert(0, {"role": "system", "content": instructions})

        if not conversation:
            raise ValueError("Must supply one of instructions/messages/input")

        return conversation

    def _build_request_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        return {key: value for key, value in kwargs.items() if value is not None}

    def _normalize_model_spec(
        self,
        model: str | Sequence[str] | "DedalusModel" | Iterable["DedalusModel"]
    ) -> str | list[str]:
        if isinstance(model, str):
            return model

        if isinstance(model, Iterable):
            models = [self._model_name(m) for m in model]
            if not models:
                raise ValueError("Model list cannot be empty")
            return models

        return self._model_name(model)

    def _model_name(self, model: Any) -> str:
        if hasattr(model, "name"):
            return model.name
        if isinstance(model, str):
            return model
        raise TypeError("Model must be a string, a DedalusModel, or an iterable of either")

    def _coerce_tool_call(self, call: ToolCall | Dict[str, Any]) -> Dict[str, Any]:
        data = _message_to_dict(call)
        fn = _message_to_dict(data.get("function", {}))
        arguments = fn.get("arguments", "{}")
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, ensure_ascii=False)

        return {
            "id": data.get("id", ""),
            "type": data.get("type", "function"),
            "function": {
                "name": fn.get("name", ""),
                "arguments": arguments,
            },
        }

    def _accumulate_tool_calls(self, deltas: Any, acc: list[Dict[str, Any]]) -> None:
        """Accumulate streaming tool call deltas into complete tool calls."""
        for delta in deltas:
            index = getattr(delta, "index", 0)

            # Ensure we have enough entries in acc
            while len(acc) <= index:
                acc.append({"id": "", "type": "function", "function": {"name": "", "arguments": ""}})

            if hasattr(delta, "id") and delta.id:
                acc[index]["id"] = delta.id
            if hasattr(delta, "function"):
                fn = delta.function
                if hasattr(fn, "name") and fn.name:
                    acc[index]["function"]["name"] = fn.name
                if hasattr(fn, "arguments") and fn.arguments:
                    acc[index]["function"]["arguments"] += fn.arguments

    def _execute_tool_calls_sync(
        self,
        tool_calls: list[Dict[str, Any]],
        tool_handler: _FunctionToolHandler,
        history: list[Message],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
        logger: _DebugLogger,
        hooks: RunnerHooks,
    ) -> None:
        for tc in tool_calls:
            name = tc["function"].get("name", "")
            args = _parse_arguments(tc["function"].get("arguments"))

            self._call_hook(hooks.on_before_tool, name, args)
            try:
                result = tool_handler.exec_sync(name, args)
                tool_results.append({"name": name, "result": result, "step": step})
                if name not in tools_called:
                    tools_called.append(name)
                history.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", ""),
                    "content": _jsonify(result),
                })
                logger.tool_execution(name, result)
                self._call_hook(hooks.on_after_tool, name, result)
            except Exception as error:  # pragma: no cover - protect caller
                tool_results.append({"name": name, "error": str(error), "step": step})
                history.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", ""),
                    "content": f"Error: {error}",
                })
                logger.tool_execution(name, error, error=True)
                self._call_hook(hooks.on_after_tool, name, error)


__all__ = [
    "DedalusRunner",
    "RunnerHooks",
]
