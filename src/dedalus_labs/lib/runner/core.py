# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import asyncio
import inspect
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Union,
    Literal,
    Callable,
    Iterator,
    Protocol,
    Sequence,
    AsyncIterator,
)
from dataclasses import field, dataclass

if TYPE_CHECKING:
    from ...types.shared.dedalus_model import DedalusModel

from ..mcp import MCPServerProtocol, serialize_mcp_servers
from .types import Message, ToolCall, JsonValue, ToolResult, PolicyInput, PolicyContext
from ..._client import Dedalus, AsyncDedalus
from ...types.shared import MCPToolResult
from ..utils._stream import accumulate_tool_call

# Type alias for mcp_servers parameter - accepts strings, server objects, or mixed lists
MCPServersInput = Union[
    str,  # Single slug or URL
    MCPServerProtocol,  # MCP server object
    Sequence[Union[str, MCPServerProtocol, Dict[str, Any]]],  # Mixed list
    None,
]
from ..utils._schemas import to_schema


def _process_policy(policy: PolicyInput, context: PolicyContext) -> Dict[str, JsonValue]:
    """Process policy, handling all possible input types safely."""
    if policy is None:
        return {}

    if callable(policy):
        try:
            result = policy(context)
            return result if isinstance(result, dict) else {}
        except Exception:
            return {}

    if isinstance(policy, dict):
        try:
            return dict(policy)
        except Exception:
            return {}

    return {}


def _extract_mcp_results(response: Any) -> list[MCPToolResult]:
    """Extract MCP tool results from API response."""
    mcp_results = getattr(response, "mcp_tool_results", None)
    if not mcp_results:
        return []
    return [item if isinstance(item, MCPToolResult) else MCPToolResult.model_validate(item) for item in mcp_results]


def _emit(callback: Callable[[Dict[str, JsonValue]], None] | None, event: Dict[str, Any]) -> None:
    """Fire a runner observation callback, swallowing any callback-side error.

    Callbacks are observation hooks; they must never break the agent loop.
    """
    if callback is None:
        return
    try:
        callback(event)
    except Exception:
        pass


def _to_jsonable(obj: Any) -> Any:
    """Convert Pydantic models and nested containers to plain JSON-friendly form.

    Used before handing event payloads to user-supplied callbacks so that
    redactors and JSON serializers see plain dicts/lists/strings, not opaque
    SDK types.
    """
    dump = getattr(obj, "model_dump", None)
    if callable(dump):
        try:
            return dump(mode="json", exclude_unset=True, by_alias=True)
        except Exception:
            pass
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    return obj


def _redact_request_for_event(request_kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Drop the credentials field before exposing request kwargs to event callbacks.

    Credentials are an out-of-band channel (API keys, tokens, signed bearer
    objects). They must never appear in trace files or be passed to
    user-supplied event callbacks, even if the underlying client accepts
    them on the model-call payload.
    """
    return {k: v for k, v in request_kwargs.items() if k != "credentials"}


def _emit_tool_ends(
    callback: Callable[[Dict[str, JsonValue]], None] | None,
    tool_calls: list,
    tool_results: list,
    prev_count: int,
    step: int,
) -> None:
    """Emit one `tool_end` event per newly-appended tool result.

    Correlates each result with its originating tool call by name (FIFO),
    so the event carries `tool_call_id` and `arguments` when available.
    """
    if callback is None:
        return
    remaining = list(tool_calls)
    for tr in tool_results[prev_count:]:
        name = tr.get("name") if isinstance(tr, dict) else None
        matched = next((c for c in remaining if c.get("function", {}).get("name") == name), None)
        if matched is not None:
            remaining.remove(matched)
        event: Dict[str, Any] = {"kind": "tool_end", "step": step, "name": name, "result": tr.get("result")}
        if isinstance(tr, dict) and tr.get("error") is not None:
            event["error"] = tr["error"]
        if matched is not None:
            event["tool_call_id"] = matched.get("id")
            event["arguments"] = matched.get("function", {}).get("arguments")
        _emit(callback, event)


class _ToolHandler(Protocol):
    def schemas(self) -> list[Dict]: ...
    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...
    def exec_sync(self, name: str, args: Dict[str, JsonValue]) -> JsonValue: ...


class _FunctionToolHandler:
    """Converts Python functions to tool handler via introspection."""

    def __init__(self, funcs: list[Callable[..., Any]]):
        self._funcs = {f.__name__: f for f in funcs}

    def schemas(self) -> list[Dict]:
        """Build OpenAI-compatible function schemas via introspection."""
        out: list[Dict[str, Any]] = []
        for fn in self._funcs.values():
            try:
                out.append(to_schema(fn))
            except Exception:
                continue
        return out

    async def exec(self, name: str, args: Dict[str, JsonValue]) -> JsonValue:
        """Execute tool by name with given args (async)."""
        fn = self._funcs[name]
        if inspect.iscoroutinefunction(fn):
            return await fn(**args)
        # asyncio.to_thread is Python 3.9+, use run_in_executor for 3.8 compat
        loop = asyncio.get_event_loop()
        # Use partial to properly pass keyword arguments
        from functools import partial

        return await loop.run_in_executor(None, partial(fn, **args))

    def exec_sync(self, name: str, args: Dict[str, JsonValue]) -> JsonValue:
        """Execute tool by name with given args (sync)."""
        fn = self._funcs[name]
        if inspect.iscoroutinefunction(fn):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(fn(**args))
            finally:
                loop.close()
        return fn(**args)


@dataclass
class _ModelConfig:
    """Model routing info + passthrough API kwargs.

    ``api_kwargs`` holds every parameter destined for the chat
    completions API (temperature, reasoning_effort, thinking, etc.).
    The runner doesn't interpret most of them — it just forwards
    them to ``client.chat.completions.create(**api_kwargs)``.
    """

    id: str
    model_list: list[str] | None = None
    api_kwargs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class _ExecutionConfig:
    """Configuration for tool execution behavior and policies."""

    mcp_servers: list[str | Dict[str, Any]] = field(default_factory=list)  # Wire format
    credentials: list[Any] | None = None  # CredentialProtocol objects (not serialized)
    max_steps: int = 10
    stream: bool = False
    transport: Literal["http", "realtime"] = "http"
    verbose: bool = False
    debug: bool = False
    on_tool_event: Callable[[Dict[str, JsonValue]], None] | None = None
    on_model_event: Callable[[Dict[str, JsonValue]], None] | None = None
    return_intent: bool = False
    policy: PolicyInput = None
    available_models: list[str] = field(default_factory=list)
    strict_models: bool = True


@dataclass
class _RunResult:
    """Result from a completed tool execution run."""

    final_output: str  # Final text output from conversation
    tool_results: list[ToolResult]
    steps_used: int
    messages: list[Message] = field(default_factory=list)  # Full conversation history
    intents: list[Dict[str, JsonValue]] | None = None
    tools_called: list[str] = field(default_factory=list)
    mcp_results: list[MCPToolResult] = field(default_factory=list)
    """MCP tool results from server-side tool calls."""

    @property
    def output(self) -> str:
        """Alias for final_output."""
        return self.final_output

    @property
    def content(self) -> str:
        """Alias for final_output."""
        return self.final_output

    def to_input_list(self) -> list[Message]:
        """Get the full conversation history for continuation."""
        return list(self.messages)


def _collect_api_kwargs(**params: Any) -> Dict[str, Any]:
    """Build API kwargs dict from explicit params, filtering out Nones."""
    return {k: v for k, v in params.items() if v is not None}


# Params that DedalusModel may carry and should be extracted.
_MODEL_EXTRACT_PARAMS = (
    "temperature",
    "max_tokens",
    "top_p",
    "frequency_penalty",
    "presence_penalty",
    "logit_bias",
    "tool_choice",
    "reasoning_effort",
    "thinking",
    "n",
    "stop",
    "stream_options",
    "logprobs",
    "top_logprobs",
    "seed",
    "service_tier",
    "parallel_tool_calls",
    "user",
    "max_completion_tokens",
)


def _extract_from_dedalus_model(
    model_obj: Any,
    api_kwargs: Dict[str, Any],
) -> bool:
    """Extract params from a DedalusModel into api_kwargs.

    Explicit values already in api_kwargs take precedence.
    Returns True if stream should be overridden from the model.
    """
    for param in _MODEL_EXTRACT_PARAMS:
        if param not in api_kwargs:
            val = getattr(model_obj, param, None)
            if val is not None:
                api_kwargs[param] = val

    # Dedalus-specific: attributes → agent_attributes
    if "agent_attributes" not in api_kwargs:
        attrs = getattr(model_obj, "attributes", None)
        if attrs:
            api_kwargs["agent_attributes"] = attrs

    return getattr(model_obj, "stream", False)


def _parse_model(
    model: Any,
    api_kwargs: Dict[str, Any],
    stream: bool,
) -> tuple:
    """Parse model param into (model_name, model_list, stream).

    Handles strings, DedalusModel objects, and lists of either.
    Extracts model-embedded params into api_kwargs.
    """
    if isinstance(model, list):
        if not model:
            raise ValueError("model list cannot be empty")
        model_name = None
        model_list = []
        for m in model:
            if hasattr(m, "name"):
                model_list.append(m.name)
                if model_name is None:
                    model_name = m.name
                    model_stream = _extract_from_dedalus_model(m, api_kwargs)
                    if not stream:
                        stream = model_stream
            else:
                model_list.append(m)
                if model_name is None:
                    model_name = m
        return model_name, model_list, stream

    if hasattr(model, "name"):
        model_stream = _extract_from_dedalus_model(model, api_kwargs)
        if not stream:
            stream = model_stream
        return model.name, [model.name], stream

    return model, [model] if model else [], stream


class DedalusRunner:
    """Enhanced Dedalus client with tool execution capabilities."""

    def __init__(self, client: Dedalus | AsyncDedalus, verbose: bool = False):
        self.client = client
        self.verbose = verbose

    def run(
        self,
        input: str | list[Message] | None = None,
        tools: list[Callable] | None = None,
        messages: list[Message] | None = None,
        instructions: str | None = None,
        model: str | list[str] | DedalusModel | list[DedalusModel] | None = None,
        # --- Runner config ---
        max_steps: int = 10,
        mcp_servers: MCPServersInput = None,
        credentials: Sequence[Any] | None = None,
        stream: bool = False,
        transport: Literal["http", "realtime"] = "http",
        verbose: bool | None = None,
        debug: bool | None = None,
        on_tool_event: Callable[[Dict[str, JsonValue]], None] | None = None,
        on_model_event: Callable[[Dict[str, JsonValue]], None] | None = None,
        return_intent: bool = False,
        policy: PolicyInput = None,
        available_models: list[str] | None = None,
        strict_models: bool = True,
        agent_attributes: Dict[str, float] | None = None,
        audio: Dict[str, Any] | None = None,
        cached_content: str | None = None,
        deferred: bool | None = None,
        frequency_penalty: float | None = None,
        function_call: str | None = None,
        generation_config: Dict[str, Any] | None = None,
        guardrails: list[Dict[str, JsonValue]] | None = None,
        handoff_config: Dict[str, JsonValue] | None = None,
        logit_bias: Dict[str, int] | None = None,
        logprobs: bool | None = None,
        max_completion_tokens: int | None = None,
        max_tokens: int | None = None,
        metadata: Dict[str, Any] | None = None,
        modalities: list[str] | None = None,
        model_attributes: Dict[str, Dict[str, float]] | None = None,
        n: int | None = None,
        parallel_tool_calls: bool | None = None,
        prediction: Dict[str, Any] | None = None,
        presence_penalty: float | None = None,
        prompt_cache_key: str | None = None,
        prompt_cache_retention: str | None = None,
        prompt_mode: str | None = None,
        reasoning_effort: str | None = None,
        response_format: Dict[str, JsonValue] | type | None = None,
        safe_prompt: bool | None = None,
        safety_identifier: str | None = None,
        safety_settings: list[Dict[str, Any]] | None = None,
        search_parameters: Dict[str, Any] | None = None,
        seed: int | None = None,
        service_tier: str | None = None,
        stop: str | list[str] | None = None,
        store: bool | None = None,
        stream_options: Dict[str, Any] | None = None,
        system_instruction: str | Dict[str, Any] | None = None,
        temperature: float | None = None,
        thinking: Dict[str, Any] | None = None,
        tool_choice: str | Dict[str, JsonValue] | None = None,
        tool_config: Dict[str, Any] | None = None,
        top_k: int | None = None,
        top_logprobs: int | None = None,
        top_p: float | None = None,
        user: str | None = None,
        verbosity: str | None = None,
        web_search_options: Dict[str, Any] | None = None,
    ):
        """Execute a tool-enabled conversation.

        All parameters from the chat completions API are accepted and
        forwarded to the server verbatim. See ``CompletionCreateParamsBase``
        for full documentation of each parameter.
        """
        if not model:
            raise ValueError("model must be provided")

        # Validate tools parameter
        if tools is not None:
            if not isinstance(tools, list):
                msg = "tools must be a list of callable functions or None"
                raise ValueError(msg)

            for i, tool in enumerate(tools):
                if not callable(tool):
                    if isinstance(tool, list):
                        msg = f"tools[{i}] is a list, not a callable function. Did you mean to pass tools={tool} instead of tools=[{tool}]?"
                        raise TypeError(msg)
                    msg = (
                        f"tools[{i}] is not callable (got {type(tool).__name__}). All tools must be callable functions."
                    )
                    raise TypeError(msg)

        # Collect all API kwargs, filtering out Nones.
        api_kwargs = _collect_api_kwargs(
            agent_attributes=agent_attributes,
            audio=audio,
            cached_content=cached_content,
            deferred=deferred,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            generation_config=generation_config,
            guardrails=guardrails,
            handoff_config=handoff_config,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            modalities=modalities,
            model_attributes=model_attributes,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            prediction=prediction,
            presence_penalty=presence_penalty,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            prompt_mode=prompt_mode,
            reasoning_effort=reasoning_effort,
            response_format=response_format,
            safe_prompt=safe_prompt,
            safety_identifier=safety_identifier,
            safety_settings=safety_settings,
            search_parameters=search_parameters,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            system_instruction=system_instruction,
            temperature=temperature,
            thinking=thinking,
            tool_choice=tool_choice,
            tool_config=tool_config,
            top_k=top_k,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            verbosity=verbosity,
            web_search_options=web_search_options,
        )

        # Parse model to extract name, list, and any model-embedded params.
        model_name, model_list, stream = _parse_model(model, api_kwargs, stream)

        available_models = model_list if available_models is None else available_models

        model_config = _ModelConfig(
            id=str(model_name),
            model_list=model_list,
            api_kwargs=api_kwargs,
        )

        # Serialize mcp_servers to wire format
        serialized_mcp_servers = serialize_mcp_servers(mcp_servers)

        exec_config = _ExecutionConfig(
            mcp_servers=serialized_mcp_servers,
            credentials=list(credentials) if credentials else None,
            max_steps=max_steps,
            stream=stream,
            transport=transport,
            verbose=verbose if verbose is not None else self.verbose,
            debug=debug or False,
            on_tool_event=on_tool_event,
            on_model_event=on_model_event,
            return_intent=return_intent,
            policy=policy,
            available_models=available_models or [],
            strict_models=strict_models,
        )

        tool_handler = _FunctionToolHandler(list(tools or []))

        # Handle instructions and messages parameters
        if instructions is not None and messages is not None:
            # instructions overrides any existing system messages
            conversation = [{"role": "system", "content": instructions}] + [
                msg for msg in messages if msg.get("role") != "system"
            ]
        elif instructions is not None:
            # Convert instructions to system message, optionally with user input
            if input is not None:
                if isinstance(input, str):
                    conversation = [
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": input},
                    ]
                else:
                    conversation = [{"role": "system", "content": instructions}] + list(input)
            else:
                conversation = [{"role": "system", "content": instructions}]
        elif messages is not None:
            conversation = messages
        elif input is not None:
            conversation = [{"role": "user", "content": input}] if isinstance(input, str) else input
        else:
            raise ValueError("Must provide one of: 'instructions', 'messages', or 'input'")

        return self._execute_conversation(conversation, tool_handler, model_config, exec_config)

    def _execute_conversation(
        self,
        messages: list[Message],
        tool_handler: _ToolHandler,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ):
        """Execute conversation with unified logic for all client/streaming combinations."""
        is_async = isinstance(self.client, AsyncDedalus)

        if is_async:
            if exec_config.stream:
                return self._execute_streaming_async(messages, tool_handler, model_config, exec_config)
            else:
                return self._execute_turns_async(messages, tool_handler, model_config, exec_config)
        else:
            if exec_config.stream:
                return self._execute_streaming_sync(messages, tool_handler, model_config, exec_config)
            else:
                return self._execute_turns_sync(messages, tool_handler, model_config, exec_config)

    async def _execute_turns_async(
        self,
        messages: list[Message],
        tool_handler: _ToolHandler,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ) -> _RunResult:
        """Execute async non-streaming conversation."""
        messages = list(messages)
        steps = 0
        final_text = ""
        tool_results: list[ToolResult] = []
        tools_called: list[str] = []

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"Step started: Step={steps}")
                # Show what models are configured
                if model_config.model_list and len(model_config.model_list) > 1:
                    print(f"  Available models: {model_config.model_list}")
                    print(f"    Primary model: {model_config.id}")
                else:
                    print(f"  Using model: {model_config.id}")

            # Apply policy and get model params
            policy_result = self._apply_policy(
                exec_config.policy,
                {
                    "step": steps,
                    "messages": messages,
                    "model": model_config.id,
                    "mcp_servers": exec_config.mcp_servers,
                    "tools": list(getattr(tool_handler, "_funcs", {}).keys()),
                    "available_models": exec_config.available_models,
                },
                model_config,
                exec_config,
            )

            # Make model call
            current_messages = self._build_messages(messages, policy_result["prepend"], policy_result["append"])

            request_kwargs = {
                "model": policy_result["model"],
                "messages": current_messages,
                "tools": tool_handler.schemas() or None,
                "mcp_servers": policy_result["mcp_servers"],
                "credentials": exec_config.credentials,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            }
            _emit(exec_config.on_model_event, {"kind": "model_request", "step": steps, "request": _to_jsonable(_redact_request_for_event(request_kwargs))})
            response = await self.client.chat.completions.create(**request_kwargs)
            _emit(exec_config.on_model_event, {"kind": "model_response", "step": steps, "response": _to_jsonable(response)})

            if exec_config.verbose:
                actual_model = policy_result["model"]
                if isinstance(actual_model, list):
                    print(f"  API called with model list: {actual_model}")
                else:
                    print(f"  API called with single model: {actual_model}")
                print(f"  Response received (server says model: {getattr(response, 'model', 'unknown')})")
                print(f"    Response type: {type(response).__name__}")
                # Surface agent timeline if server included it
                agents_used = getattr(response, "agents_used", None)
                if not agents_used:
                    extra = getattr(response, "__pydantic_extra__", None)
                    if isinstance(extra, dict):
                        agents_used = extra.get("agents_used")
                if agents_used:
                    print(f" [EVENT] agents_used: {agents_used}")

            # Check if we have tool calls
            if not hasattr(response, "choices") or not response.choices:
                final_text = ""
                break

            message = response.choices[0].message
            msg = vars(message) if hasattr(message, "__dict__") else message
            tool_calls = msg.get("tool_calls")
            content = msg.get("content", "")

            if exec_config.verbose:
                print(f" Response content: {content[:100] if content else '(none)'}...")
                if tool_calls:
                    call_names = []
                    for tc in tool_calls:
                        try:
                            if isinstance(tc, dict):
                                call_names.append(tc.get("function", {}).get("name", "?"))
                            else:
                                call_names.append(getattr(getattr(tc, "function", None), "name", "?"))
                        except Exception:
                            call_names.append("?")
                    print(f" Tool calls in response: {call_names}")

            if not tool_calls:
                final_text = content or ""
                # Add assistant response to conversation
                if final_text:
                    messages.append({"role": "assistant", "content": final_text})
                break

            # Execute tools
            tool_calls = self._extract_tool_calls(response.choices[0])
            if exec_config.verbose:
                print(f" Extracted {len(tool_calls)} tool calls")
                for tc in tool_calls:
                    print(f"  - {tc.get('function', {}).get('name', '?')} (id: {tc.get('id', '?')})")
            prev_tool_count = len(tool_results)
            await self._execute_tool_calls(
                tool_calls,
                tool_handler,
                messages,
                tool_results,
                tools_called,
                steps,
                verbose=exec_config.verbose,
            )
            _emit_tool_ends(exec_config.on_tool_event, tool_calls, tool_results, prev_tool_count, steps)

        # Extract MCP tool executions from the last response
        mcp_results = _extract_mcp_results(response)

        return _RunResult(
            final_output=final_text,
            tool_results=tool_results,
            steps_used=steps,
            tools_called=tools_called,
            messages=messages,
            mcp_results=mcp_results,
        )

    async def _execute_streaming_async(
        self,
        messages: list[Message],
        tool_handler: _ToolHandler,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ) -> AsyncIterator[Any]:
        """Execute async streaming conversation."""
        messages = list(messages)
        steps = 0

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"Step started: Step={steps} (max_steps={exec_config.max_steps})")
                print(f" Starting step {steps} with {len(messages)} messages in conversation")
                print(f" Message history:")
                for i, msg in enumerate(messages):
                    role = msg.get("role")
                    content = str(msg.get("content", ""))[:50] + "..." if msg.get("content") else ""
                    tool_info = ""
                    if msg.get("tool_calls"):
                        tool_names = [tc.get("function", {}).get("name", "?") for tc in msg.get("tool_calls", [])]
                        tool_info = f" [calling: {', '.join(tool_names)}]"
                    elif msg.get("tool_call_id"):
                        tool_info = f" [response to: {msg.get('tool_call_id')[:8]}...]"
                    print(f"  [Message {i}] {role}: {content}{tool_info}")

            # Apply policy
            policy_result = self._apply_policy(
                exec_config.policy,
                {
                    "step": steps,
                    "messages": messages,
                    "model": model_config.id,
                    "mcp_servers": exec_config.mcp_servers,
                    "tools": list(getattr(tool_handler, "_funcs", {}).keys()),
                    "available_models": exec_config.available_models,
                },
                model_config,
                exec_config,
            )

            # Stream model response
            current_messages = self._build_messages(messages, policy_result["prepend"], policy_result["append"])

            # Suppress per-message debug; keep streaming minimal

            stream = await self.client.chat.completions.create(
                model=policy_result["model"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                credentials=exec_config.credentials,
                stream=True,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

            tool_calls = []
            chunk_count = 0
            content_chunks = 0
            tool_call_chunks = 0
            finish_reason = None
            mcp_tool_results_from_server: list = []
            async for chunk in stream:
                chunk_count += 1
                if exec_config.verbose:
                    # Only surface agent_updated metadata; suppress raw chunk spam
                    extra = getattr(chunk, "__pydantic_extra__", None)
                    if isinstance(extra, dict):
                        meta = extra.get("x_dedalus_event") or extra.get("dedalus_event")
                        if isinstance(meta, dict) and meta.get("type") == "agent_updated":
                            print(f" [EVENT] agent_updated: agent={meta.get('agent')} model={meta.get('model')}")

                # Collect MCP tool results emitted by the server
                chunk_extra = getattr(chunk, "__pydantic_extra__", None) or {}
                if isinstance(chunk_extra, dict) and "mcp_tool_results" in chunk_extra:
                    mcp_tool_results_from_server = chunk_extra["mcp_tool_results"]

                if hasattr(chunk, "choices") and chunk.choices:
                    choice = chunk.choices[0]
                    delta = choice.delta

                    # Check finish reason
                    if hasattr(choice, "finish_reason") and choice.finish_reason:
                        finish_reason = choice.finish_reason
                        # suppress per-chunk finish_reason spam

                    # Check for tool calls
                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        tool_call_chunks += 1
                        self._accumulate_tool_calls(delta.tool_calls, tool_calls)
                        # suppress per-chunk tool_call delta spam

                    # Check for content
                    if hasattr(delta, "content") and delta.content:
                        content_chunks += 1
                        # suppress per-chunk content spam

                    # Check for role (suppressed)
                    if hasattr(delta, "role") and delta.role:
                        pass

                    yield chunk

            if exec_config.verbose:
                # Keep a compact end-of-stream summary
                names = [tc.get("function", {}).get("name", "unknown") for tc in tool_calls]
                print(f" Stream summary: chunks={chunk_count} content={content_chunks} tool_calls={tool_call_chunks}")
                if names:
                    print(f" Tools called this turn: {names}")

            # Execute any accumulated tool calls
            if tool_calls:
                if exec_config.verbose:
                    print(f" Processing {len(tool_calls)} tool calls")

                # Categorize tools
                local_names = [
                    tc["function"]["name"]
                    for tc in tool_calls
                    if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                ]
                mcp_names = [
                    tc["function"]["name"]
                    for tc in tool_calls
                    if tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})
                ]

                # Check if ALL tools are MCP tools (none are local)
                all_mcp = all(tc["function"]["name"] not in getattr(tool_handler, "_funcs", {}) for tc in tool_calls)

                # Check if stream already contains content (MCP results)
                has_streamed_content = content_chunks > 0

                if exec_config.verbose:
                    print(f" Local tools used: {local_names}")
                    print(f" Server tools used: {mcp_names}")

                # All tools are server side and results have already been streamed.
                if all_mcp and has_streamed_content:
                    if exec_config.verbose:
                        print(f" All tools are MCP and content streamed, breaking loop")
                    break

                # At least one local tool exists. Execute via the dependency aware scheduler.
                if not all_mcp:
                    local_only = [
                        tc for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]

                    from ._scheduler import execute_local_tools_async

                    await execute_local_tools_async(
                        local_only,
                        tool_handler,
                        messages,
                        [],
                        [],
                        steps,
                        verbose=exec_config.verbose,
                    )

                    if exec_config.verbose:
                        print(f" Messages after tool execution: {len(messages)}")
            else:
                if exec_config.verbose:
                    print(f" No tool calls found, breaking out of loop")
                break

        if exec_config.verbose:
            print(f"\n[DEBUG] Exited main loop after {steps} steps")

    def _execute_turns_sync(
        self,
        messages: list[Message],
        tool_handler: _ToolHandler,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ) -> _RunResult:
        """Execute sync non-streaming conversation."""
        messages = list(messages)
        steps = 0
        final_text = ""
        tool_results: list[ToolResult] = []
        tools_called: list[str] = []

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"Step started: Step={steps}")
                # Show what models are configured
                if model_config.model_list and len(model_config.model_list) > 1:
                    print(f"  Available models: {model_config.model_list}")
                    print(f"    Primary model: {model_config.id}")
                else:
                    print(f"  Using model: {model_config.id}")

            # Apply policy
            policy_result = self._apply_policy(
                exec_config.policy,
                {
                    "step": steps,
                    "messages": messages,
                    "model": model_config.id,
                    "mcp_servers": exec_config.mcp_servers,
                    "tools": list(getattr(tool_handler, "_funcs", {}).keys()),
                    "available_models": exec_config.available_models,
                },
                model_config,
                exec_config,
            )

            # Make model call
            current_messages = self._build_messages(messages, policy_result["prepend"], policy_result["append"])

            if exec_config.verbose:
                actual_model = policy_result["model"]
                if isinstance(actual_model, list):
                    print(f"  API called with model list: {actual_model}")
                else:
                    print(f"  API called with single model: {actual_model}")

            request_kwargs = {
                "model": policy_result["model"],
                "messages": current_messages,
                "tools": tool_handler.schemas() or None,
                "mcp_servers": policy_result["mcp_servers"],
                "credentials": exec_config.credentials,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            }
            _emit(exec_config.on_model_event, {"kind": "model_request", "step": steps, "request": _to_jsonable(_redact_request_for_event(request_kwargs))})
            response = self.client.chat.completions.create(**request_kwargs)
            _emit(exec_config.on_model_event, {"kind": "model_response", "step": steps, "response": _to_jsonable(response)})

            if exec_config.verbose:
                print(f"  Response received (server says model: {getattr(response, 'model', 'unknown')})")
                print(f"    Response type: {type(response).__name__}")

            # Check if we have tool calls
            if not hasattr(response, "choices") or not response.choices:
                final_text = ""
                break

            message = response.choices[0].message
            msg = vars(message) if hasattr(message, "__dict__") else message
            tool_calls = msg.get("tool_calls")
            content = msg.get("content", "")

            if exec_config.verbose:
                print(f"  Response content: {content[:100] if content else '(none)'}...")
                if tool_calls:
                    tool_names = [tc.get("function", {}).get("name", "?") for tc in tool_calls]
                    print(f" 🔧 Tool calls in response: {tool_names}")

            if not tool_calls:
                final_text = content or ""
                # Add assistant response to conversation
                if final_text:
                    messages.append({"role": "assistant", "content": final_text})
                break

            # Execute tools
            tool_calls = self._extract_tool_calls(response.choices[0])
            prev_tool_count = len(tool_results)
            self._execute_tool_calls_sync(tool_calls, tool_handler, messages, tool_results, tools_called, steps)
            _emit_tool_ends(exec_config.on_tool_event, tool_calls, tool_results, prev_tool_count, steps)

        # Extract MCP tool executions from the last response
        mcp_results = _extract_mcp_results(response)

        return _RunResult(
            final_output=final_text,
            tool_results=tool_results,
            steps_used=steps,
            tools_called=tools_called,
            messages=messages,
            mcp_results=mcp_results,
        )

    def _execute_streaming_sync(
        self,
        messages: list[Message],
        tool_handler: _ToolHandler,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ) -> Iterator[Any]:
        """Execute sync streaming conversation."""
        messages = list(messages)
        steps = 0

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"Step started: Step={steps} (max_steps={exec_config.max_steps})")
                print(f" Starting step {steps} with {len(messages)} messages in conversation")
                print(f" Message history:")
                for i, msg in enumerate(messages):
                    role = msg.get("role")
                    content = str(msg.get("content", ""))[:50] + "..." if msg.get("content") else ""
                    tool_info = ""
                    if msg.get("tool_calls"):
                        tool_names = [tc.get("function", {}).get("name", "?") for tc in msg.get("tool_calls", [])]
                        tool_info = f" [calling: {', '.join(tool_names)}]"
                    elif msg.get("tool_call_id"):
                        tool_info = f" [response to: {msg.get('tool_call_id')[:8]}...]"
                    print(f"  [Message {i}] {role}: {content}{tool_info}")

            # Apply policy
            policy_result = self._apply_policy(
                exec_config.policy,
                {
                    "step": steps,
                    "messages": messages,
                    "model": model_config.id,
                    "mcp_servers": exec_config.mcp_servers,
                    "tools": list(getattr(tool_handler, "_funcs", {}).keys()),
                    "available_models": exec_config.available_models,
                },
                model_config,
                exec_config,
            )

            # Stream model response
            current_messages = self._build_messages(messages, policy_result["prepend"], policy_result["append"])

            if exec_config.verbose:
                print(f" Messages being sent to API:")
                for i, msg in enumerate(current_messages):
                    content_preview = str(msg.get("content", ""))[:100]
                    tool_call_info = ""
                    if msg.get("tool_calls"):
                        tool_names = [tc.get("function", {}).get("name", "unknown") for tc in msg.get("tool_calls", [])]
                        tool_call_info = f" tool_calls=[{', '.join(tool_names)}]"
                    print(f"  [{i}] {msg.get('role')}: {content_preview}...{tool_call_info}")
                print(f" MCP servers: {policy_result['mcp_servers']}")
                print(f" Local tools available: {list(getattr(tool_handler, '_funcs', {}).keys())}")

            stream = self.client.chat.completions.create(
                model=policy_result["model"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                credentials=exec_config.credentials,
                stream=True,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

            tool_calls = []
            chunk_count = 0
            content_chunks = 0
            tool_call_chunks = 0
            finish_reason = None
            accumulated_content = ""
            mcp_tool_results_from_server: list = []

            for chunk in stream:
                chunk_count += 1

                # Collect MCP tool results emitted by the server
                chunk_extra = getattr(chunk, "__pydantic_extra__", None) or {}
                if isinstance(chunk_extra, dict) and "mcp_tool_results" in chunk_extra:
                    mcp_tool_results_from_server = chunk_extra["mcp_tool_results"]

                if hasattr(chunk, "choices") and chunk.choices:
                    choice = chunk.choices[0]
                    delta = choice.delta

                    # Check finish reason
                    if hasattr(choice, "finish_reason") and choice.finish_reason:
                        finish_reason = choice.finish_reason

                    # Check for tool calls
                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        tool_call_chunks += 1
                        self._accumulate_tool_calls(delta.tool_calls, tool_calls)
                        if exec_config.verbose:
                            # Show tool calls in a more readable format
                            for tc_delta in delta.tool_calls:
                                if (
                                    hasattr(tc_delta, "function")
                                    and hasattr(tc_delta.function, "name")
                                    and tc_delta.function.name
                                ):
                                    print(f"-> Calling {tc_delta.function.name}")

                    # Check for content
                    if hasattr(delta, "content") and delta.content:
                        content_chunks += 1
                        accumulated_content += delta.content

                    yield chunk

            if exec_config.verbose:
                if accumulated_content:
                    print()  # New line after streamed content
                if tool_calls:
                    print(f"\nReceived {len(tool_calls)} tool call(s)")
                    for i, tc in enumerate(tool_calls, 1):
                        tool_name = tc.get("function", {}).get("name", "unknown")
                        # Clean up the tool name for display
                        display_name = tool_name.replace("transfer_to_", "").replace("_", " ").title()
                        print(f"   {i}. {display_name}")
                else:
                    print(f"\n✓ Response complete ({content_chunks} content chunks)")

            # Execute any accumulated tool calls
            if tool_calls:
                if exec_config.verbose:
                    print(f" Processing {len(tool_calls)} tool calls")

                # Categorize tools
                local_names = [
                    tc["function"]["name"]
                    for tc in tool_calls
                    if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                ]
                mcp_names = [
                    tc["function"]["name"]
                    for tc in tool_calls
                    if tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})
                ]

                # Check if ALL tools are MCP tools (none are local)
                all_mcp = all(tc["function"]["name"] not in getattr(tool_handler, "_funcs", {}) for tc in tool_calls)

                # Check if stream already contains content (MCP results)
                has_streamed_content = content_chunks > 0

                if exec_config.verbose:
                    print(f"  Local tools: {local_names}")
                    print(f"  Server tools: {mcp_names}")

                # All tools are server side and results have already been streamed.
                if all_mcp and has_streamed_content:
                    if exec_config.verbose:
                        print(f"  All tools are MCP and content streamed, breaking loop")
                    break

                # At least one local tool exists. Execute via the dependency aware scheduler.
                if not all_mcp:
                    local_only = [
                        tc for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]

                    from ._scheduler import execute_local_tools_sync

                    execute_local_tools_sync(
                        local_only,
                        tool_handler,
                        messages,
                        [],
                        [],
                        steps,
                    )

                    if exec_config.verbose:
                        print(f"  Messages after tool execution: {len(messages)}")
            else:
                if exec_config.verbose:
                    print(f" No tool calls found, breaking out of loop")
                break

    def _apply_policy(
        self,
        policy: PolicyInput,
        context: PolicyContext,
        model_config: _ModelConfig,
        exec_config: _ExecutionConfig,
    ) -> Dict[str, Any]:
        """Apply policy and return unified configuration."""
        pol = _process_policy(policy, context)

        # Start with defaults
        result = {
            "model_id": model_config.id,
            "model": model_config.model_list
            if model_config.model_list
            else model_config.id,  # Use full list when available
            "mcp_servers": list(exec_config.mcp_servers),
            "model_kwargs": {},
            "prepend": [],
            "append": [],
        }

        if pol:
            # Handle model override
            requested_model = pol.get("model")
            if requested_model and exec_config.strict_models and exec_config.available_models:
                if isinstance(requested_model, list):
                    # Filter to only available models
                    valid_models = [m for m in requested_model if m in exec_config.available_models]
                    if valid_models:
                        result["model"] = valid_models
                        result["model_id"] = str(valid_models[0])
                    elif exec_config.verbose:
                        print(f"[RUNNER] Policy requested unavailable models {requested_model}, ignoring")
                elif requested_model not in exec_config.available_models:
                    if exec_config.verbose:
                        print(f"[RUNNER] Policy requested unavailable model '{requested_model}', ignoring")
                else:
                    result["model_id"] = str(requested_model)
                    result["model"] = str(requested_model)
            elif requested_model:
                if isinstance(requested_model, list):
                    result["model"] = requested_model
                    result["model_id"] = str(requested_model[0]) if requested_model else result["model_id"]
                else:
                    result["model_id"] = str(requested_model)
                    result["model"] = str(requested_model)

            # Handle other policy settings
            result["mcp_servers"] = list(pol.get("mcp_servers", result["mcp_servers"]))
            result["model_kwargs"] = dict(pol.get("model_settings", {}))
            result["prepend"] = list(pol.get("message_prepend", []))
            result["append"] = list(pol.get("message_append", []))

            # Handle max_steps update
            if pol.get("max_steps") is not None:
                try:
                    exec_config.max_steps = int(pol.get("max_steps"))
                except Exception:
                    pass

        return result

    def _build_messages(self, messages: list[Message], prepend: list[Message], append: list[Message]) -> list[Message]:
        """Build final message list with prepend/append."""
        return (prepend + messages + append) if (prepend or append) else messages

    def _extract_tool_calls(self, choice) -> list[ToolCall]:
        """Extract tool calls from response choice."""
        if not hasattr(choice, "message"):
            return []

        message = choice.message
        msg = vars(message) if hasattr(message, "__dict__") else message
        tool_calls = msg.get("tool_calls", [])

        if not tool_calls:
            return []

        calls = []
        for tc in tool_calls:
            tc_dict = vars(tc) if hasattr(tc, "__dict__") else tc
            fn = tc_dict.get("function", {})
            fn_dict = vars(fn) if hasattr(fn, "__dict__") else fn

            tc_out: ToolCall = {
                "id": tc_dict.get("id", ""),
                "type": tc_dict.get("type", "function"),
                "function": {
                    "name": fn_dict.get("name", ""),
                    "arguments": fn_dict.get("arguments", "{}"),
                },
            }
            thought_sig = tc_dict.get("thought_signature")
            if thought_sig:
                tc_out["thought_signature"] = thought_sig
            calls.append(tc_out)
        return calls

    async def _execute_tool_calls(
        self,
        tool_calls: list[ToolCall],
        tool_handler: _ToolHandler,
        messages: list[Message],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
        verbose: bool = False,
    ):
        """Execute tool calls asynchronously with dependency-aware scheduling.

        Independent tools fire concurrently. Dependent tools wait for
        their prerequisites. Falls back to sequential on cyclic deps.
        """
        from ._scheduler import execute_local_tools_async

        if verbose:
            print(f" _execute_tool_calls: Processing {len(tool_calls)} tool calls")

        # Record assistant message with all tool calls (OpenAI format).
        messages.append({"role": "assistant", "tool_calls": list(tool_calls)})

        await execute_local_tools_async(
            tool_calls,
            tool_handler,
            messages,
            tool_results,
            tools_called,
            step,
            verbose=verbose,
        )

    def _execute_tool_calls_sync(
        self,
        tool_calls: list[ToolCall],
        tool_handler: _ToolHandler,
        messages: list[Message],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
    ):
        """Execute tool calls synchronously with dependency-aware ordering."""
        from ._scheduler import execute_local_tools_sync

        # Record assistant message with all tool calls (OpenAI format).
        messages.append({"role": "assistant", "tool_calls": list(tool_calls)})

        execute_local_tools_sync(
            tool_calls,
            tool_handler,
            messages,
            tool_results,
            tools_called,
            step,
        )

    def _accumulate_tool_calls(self, deltas, acc: list[ToolCall]) -> None:
        """Accumulate streaming tool call deltas."""
        for delta in deltas:
            accumulate_tool_call(acc, delta)

    @staticmethod
    def _mk_kwargs(mc: _ModelConfig) -> Dict[str, Any]:
        """Convert model config to kwargs for the API call."""
        from ..._utils import is_given
        from ...lib._parsing import type_to_response_format_param

        kwargs = dict(mc.api_kwargs)

        # Convert Pydantic model class to dict schema if needed.
        if "response_format" in kwargs and kwargs["response_format"] is not None:
            converted = type_to_response_format_param(kwargs["response_format"])
            kwargs["response_format"] = converted if is_given(converted) else None

        return {k: v for k, v in kwargs.items() if v is not None}
