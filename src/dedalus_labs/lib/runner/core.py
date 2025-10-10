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
from typing import TYPE_CHECKING, Any, Dict, Callable, Iterable, Protocol, Sequence
from dataclasses import field, dataclass

from dedalus_labs import Dedalus, AsyncDedalus

if TYPE_CHECKING:  # pragma: no cover - optional runtime dependency
    from ...types.dedalus_model import DedalusModel

from .types import Message, ToolCall, JsonValue, ToolResult, PolicyInput, PolicyContext
from ..utils import to_schema


@dataclass
class GuardrailCheckResult:
    tripwire_triggered: bool
    info: Any = None


GuardrailFunc = Callable[[Any], GuardrailCheckResult | bool | None]


class InputGuardrailTriggered(RuntimeError):
    def __init__(self, result: GuardrailCheckResult):
        super().__init__("Input guardrail tripwire triggered")
        self.result = result


class OutputGuardrailTriggered(RuntimeError):
    def __init__(self, result: GuardrailCheckResult):
        super().__init__("Output guardrail tripwire triggered")
        self.result = result


@dataclass
class RunnerHooks:
    on_before_run: Callable[[list[Message]], None] | None = None
    on_after_run: Callable[["_RunResult"], None] | None = None
    on_before_model_call: Callable[[dict[str, Any]], None] | None = None
    on_after_model_call: Callable[[Any], None] | None = None
    on_before_tool: Callable[[str, Dict[str, Any]], None] | None = None
    on_after_tool: Callable[[str, JsonValue | Exception], None] | None = None
    on_guardrail_trigger: Callable[[str, GuardrailCheckResult], None] | None = None


def input_guardrail(func: GuardrailFunc | None = None, *, name: str | None = None) -> GuardrailFunc | Callable[[GuardrailFunc], GuardrailFunc]:
    """Decorator used to mark a callable as an input guardrail.

    Usage mirrors the backend helpers but the callable is expected to accept the
    pre-call conversation payload (list of messages) and return either a
    `GuardrailCheckResult`, a tuple `(triggered, info)`, a boolean, or ``None``.
    """

    def decorator(fn: GuardrailFunc) -> GuardrailFunc:
        fn._guardrail_name = name or getattr(fn, "__name__", "input_guardrail")
        return fn

    if func is not None:
        return decorator(func)
    return decorator


def output_guardrail(func: GuardrailFunc | None = None, *, name: str | None = None) -> GuardrailFunc | Callable[[GuardrailFunc], GuardrailFunc]:
    """Decorator used to mark a callable as an output guardrail.

    The callable receives the final assistant message string.
    """

    def decorator(fn: GuardrailFunc) -> GuardrailFunc:
        fn._guardrail_name = name or getattr(fn, "__name__", "output_guardrail")
        return fn

    if func is not None:
        return decorator(func)
    return decorator

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _process_policy(policy: PolicyInput, context: PolicyContext) -> Dict[str, JsonValue]:
    """Safely execute/normalise a user-supplied policy callback/value."""

    if policy is None:
        return {}

    if callable(policy):
        try:
            result = policy(context)
        except Exception:  # pragma: no cover - user code
            return {}
        return result if isinstance(result, dict) else {}

    if isinstance(policy, dict):
        try:
            return dict(policy)
        except Exception:  # pragma: no cover - defensive protection
            return {}

    return {}


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

    def policy_delta(self, overrides: Dict[str, Any]) -> None:
        if self.enabled and overrides:
            self.log(f"Policy overrides: {overrides}")

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


class _ToolHandler(Protocol):
    def schemas(self) -> list[Dict[str, Any]]: ...

    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...

    def exec_sync(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...


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

    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue:
        fn = self._funcs[name]
        if inspect.iscoroutinefunction(fn):
            return await fn(**args)
        return await asyncio.to_thread(fn, **args)

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
# Runner state + policy decision
# ---------------------------------------------------------------------------


@dataclass
class _RunnerState:
    model: str | list[str]
    request_kwargs: Dict[str, Any]
    auto_execute_tools: bool
    max_steps: int
    mcp_servers: list[str]
    policy: PolicyInput
    logger: _DebugLogger
    tool_handler: _FunctionToolHandler
    input_guardrails: list[GuardrailFunc]
    output_guardrails: list[GuardrailFunc]
    hooks: RunnerHooks


@dataclass
class _PolicyDecision:
    model: str | list[str]
    mcp_servers: list[str]
    prepend: list[Message]
    append: list[Message]
    extra_kwargs: Dict[str, Any]
    max_steps_override: int | None = None


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
        policy: PolicyInput = None,
        input_guardrails: Iterable[GuardrailFunc] | None = None,
        output_guardrails: Iterable[GuardrailFunc] | None = None,
        hooks: RunnerHooks | None = None,
        _available_models: Iterable[str] | None = None,  # legacy, ignored
        _strict_models: bool = True,  # legacy, ignored
    ) -> _RunResult:
        """Run the assistant until completion or tool-call deferral."""

        if model is None:
            raise ValueError("model must be provided")

        if stream:
            raise NotImplementedError(
                "DedalusRunner no longer orchestrates streaming responses. "
                "Call client.chat.completions.create(..., stream=True) for streaming support."
            )

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
            policy=policy,
            logger=logger,
            tool_handler=tool_handler,
            input_guardrails=list(input_guardrails or []),
            output_guardrails=list(output_guardrails or []),
            hooks=hook_state,
        )

        conversation = self._initial_messages(instructions=instructions, input=input, messages=messages)
        self._call_hook(state.hooks.on_before_run, copy.deepcopy(conversation))
        input_guardrail_results = self._run_input_guardrails(conversation, state)
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

            decision = self._apply_policy(state, history, steps)
            state.logger.models(decision.model, previous_model)
            state.logger.policy_delta({
                k: v
                for k, v in {
                    "model_settings": decision.extra_kwargs,
                    "message_prepend": decision.prepend,
                    "message_append": decision.append,
                    "max_steps": decision.max_steps_override,
                }.items()
                if v
            })

            if decision.max_steps_override is not None:
                try:
                    state.max_steps = max(1, int(decision.max_steps_override))
                except ValueError:  # pragma: no cover - defensive
                    pass

            payload = decision.prepend + history + decision.append
            if state.logger.debug:
                state.logger.messages_snapshot(payload)

            request_kwargs = {**state.request_kwargs, **decision.extra_kwargs}
            self._call_hook(
                state.hooks.on_before_model_call,
                {
                    "model": decision.model,
                    "messages": payload,
                    "kwargs": request_kwargs,
                },
            )
            response = self.client.chat.completions.create(
                model=decision.model,
                messages=payload,
                tools=tool_schemas,
                mcp_servers=decision.mcp_servers or None,
                **request_kwargs,
            )
            self._call_hook(state.hooks.on_after_model_call, response)

            models_used.append(_render_model_spec(decision.model))
            previous_model = decision.model

            if not getattr(response, "choices", None):
                break

            choice = response.choices[0]
            message_dict = _message_to_dict(choice.message)
            tool_calls = message_dict.get("tool_calls") or []
            content = message_dict.get("content")

            if not tool_calls:
                final_text = content or ""
                if final_text:
                    history.append({"role": "assistant", "content": final_text})
                break

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

    # ------------------------------------------------------------------
    # Policy + helpers
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

    def _apply_policy(self, state: _RunnerState, history: list[Message], step: int) -> _PolicyDecision:
        base_context: PolicyContext = {
            "step": step,
            "messages": history,
            "model": state.model,
            "mcp_servers": state.mcp_servers,
            "tools": list(state.tool_handler._funcs.keys()),
        }
        raw = _process_policy(state.policy, base_context)

        model_override = raw.get("model")
        mcp_override = raw.get("mcp_servers")

        decision = _PolicyDecision(
            model=model_override if model_override is not None else state.model,
            mcp_servers=list(mcp_override) if mcp_override is not None else list(state.mcp_servers),
            prepend=list(raw.get("message_prepend", [])),
            append=list(raw.get("message_append", [])),
            extra_kwargs=dict(raw.get("model_settings", {})),
            max_steps_override=raw.get("max_steps"),
        )
        return decision

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
    "GuardrailCheckResult",
    "InputGuardrailTriggered",
    "OutputGuardrailTriggered",
    "RunnerHooks",
    "input_guardrail",
    "output_guardrail",
]
