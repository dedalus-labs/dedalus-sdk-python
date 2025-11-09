# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import json
import asyncio
import inspect
from typing import TYPE_CHECKING, Any, Dict, Literal, Callable, Iterator, Protocol, AsyncIterator
from dataclasses import field, asdict, dataclass

from dedalus_labs import Dedalus, AsyncDedalus

if TYPE_CHECKING:
    from ...types.dedalus_model import DedalusModel


from .types import Message, ToolCall, JsonValue, ToolResult, PolicyInput, PolicyContext
from ..utils import to_schema


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
    """Model configuration parameters."""

    id: str
    model_list: list[str] | None = None  # Store the full model list when provided
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    logit_bias: Dict[str, int] | None = None
    response_format: Dict[str, JsonValue] | type | None = None  # Dict or Pydantic model
    agent_attributes: Dict[str, float] | None = None
    model_attributes: Dict[str, Dict[str, float]] | None = None
    tool_choice: str | Dict[str, JsonValue] | None = None
    guardrails: list[Dict[str, JsonValue]] | None = None
    handoff_config: Dict[str, JsonValue] | None = None


@dataclass
class _ExecutionConfig:
    """Configuration for tool execution behavior and policies."""

    mcp_servers: list[str] = field(default_factory=list)
    max_steps: int = 10
    stream: bool = False
    transport: Literal["http", "realtime"] = "http"
    verbose: bool = False
    debug: bool = False
    on_tool_event: Callable[[Dict[str, JsonValue]], None] | None = None
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
        max_steps: int = 10,
        mcp_servers: str | list[str] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        logit_bias: Dict[str, int] | None = None,
        response_format: Dict[str, JsonValue] | type | None = None,
        stream: bool = False,
        transport: Literal["http", "realtime"] = "http",
        verbose: bool | None = None,
        debug: bool | None = None,
        on_tool_event: Callable[[Dict[str, JsonValue]], None] | None = None,
        return_intent: bool = False,
        agent_attributes: Dict[str, float] | None = None,
        model_attributes: Dict[str, Dict[str, float]] | None = None,
        tool_choice: str | Dict[str, JsonValue] | None = None,
        guardrails: list[Dict[str, JsonValue]] | None = None,
        handoff_config: Dict[str, JsonValue] | None = None,
        policy: PolicyInput = None,
        available_models: list[str] | None = None,
        strict_models: bool = True,
    ):
        """Execute tools with unified async/sync + streaming/non-streaming logic."""
        if not model:
            raise ValueError("model must be provided")

        # Validate tools parameter
        if tools is not None:
            if not isinstance(tools, list):
                msg = "tools must be a list of callable functions or None"
                raise ValueError(msg)

            # Check for nested lists (common mistake: tools=[[]] instead of tools=[])
            for i, tool in enumerate(tools):
                if not callable(tool):
                    if isinstance(tool, list):
                        msg = f"tools[{i}] is a list, not a callable function. Did you mean to pass tools={tool} instead of tools=[{tool}]?"
                        raise TypeError(msg)
                    msg = f"tools[{i}] is not callable (got {type(tool).__name__}). All tools must be callable functions."
                    raise TypeError(msg)

        # Parse model to extract name and config
        model_name = None
        model_list = []

        if isinstance(model, list):
            if not model:
                raise ValueError("model list cannot be empty")
            # Handle list of DedalusModel or strings
            for m in model:
                if hasattr(m, "name"):  # DedalusModel
                    model_list.append(m.name)
                    # Use config from first DedalusModel if params not explicitly set
                    if model_name is None:
                        model_name = m.name
                        temperature = temperature if temperature is not None else getattr(m, "temperature", None)
                        max_tokens = max_tokens if max_tokens is not None else getattr(m, "max_tokens", None)
                        top_p = top_p if top_p is not None else getattr(m, "top_p", None)
                        frequency_penalty = (
                            frequency_penalty
                            if frequency_penalty is not None
                            else getattr(m, "frequency_penalty", None)
                        )
                        presence_penalty = (
                            presence_penalty if presence_penalty is not None else getattr(m, "presence_penalty", None)
                        )
                        logit_bias = logit_bias if logit_bias is not None else getattr(m, "logit_bias", None)

                        # Extract additional parameters from first DedalusModel
                        stream = stream if stream is not False else getattr(m, "stream", False)
                        tool_choice = tool_choice if tool_choice is not None else getattr(m, "tool_choice", None)

                        # Extract Dedalus-specific extensions
                        if hasattr(m, "attributes") and m.attributes:
                            agent_attributes = agent_attributes if agent_attributes is not None else m.attributes

                        # Check for unsupported parameters (only warn once for first model)
                        unsupported_params = []
                        if hasattr(m, "n") and m.n is not None:
                            unsupported_params.append("n")
                        if hasattr(m, "stop") and m.stop is not None:
                            unsupported_params.append("stop")
                        if hasattr(m, "stream_options") and m.stream_options is not None:
                            unsupported_params.append("stream_options")
                        if hasattr(m, "logprobs") and m.logprobs is not None:
                            unsupported_params.append("logprobs")
                        if hasattr(m, "top_logprobs") and m.top_logprobs is not None:
                            unsupported_params.append("top_logprobs")
                        if hasattr(m, "seed") and m.seed is not None:
                            unsupported_params.append("seed")
                        if hasattr(m, "service_tier") and m.service_tier is not None:
                            unsupported_params.append("service_tier")
                        if hasattr(m, "tools") and m.tools is not None:
                            unsupported_params.append("tools")
                        if hasattr(m, "parallel_tool_calls") and m.parallel_tool_calls is not None:
                            unsupported_params.append("parallel_tool_calls")
                        if hasattr(m, "user") and m.user is not None:
                            unsupported_params.append("user")
                        if hasattr(m, "max_completion_tokens") and m.max_completion_tokens is not None:
                            unsupported_params.append("max_completion_tokens")

                        if unsupported_params:
                            import warnings

                            warnings.warn(
                                f"The following DedalusModel parameters are not yet supported and will be ignored: {', '.join(unsupported_params)}. "
                                f"Support for these parameters is coming soon.",
                                UserWarning,
                                stacklevel=2,
                            )
                else:  # String
                    model_list.append(m)
                    if model_name is None:
                        model_name = m
        elif hasattr(model, "name"):  # Single DedalusModel
            model_name = model.name
            model_list = [model.name]
            # Extract config from DedalusModel if params not explicitly set
            temperature = temperature if temperature is not None else getattr(model, "temperature", None)
            max_tokens = max_tokens if max_tokens is not None else getattr(model, "max_tokens", None)
            top_p = top_p if top_p is not None else getattr(model, "top_p", None)
            frequency_penalty = (
                frequency_penalty if frequency_penalty is not None else getattr(model, "frequency_penalty", None)
            )
            presence_penalty = (
                presence_penalty if presence_penalty is not None else getattr(model, "presence_penalty", None)
            )
            logit_bias = logit_bias if logit_bias is not None else getattr(model, "logit_bias", None)

            # Extract additional supported parameters
            stream = stream if stream is not False else getattr(model, "stream", False)
            tool_choice = tool_choice if tool_choice is not None else getattr(model, "tool_choice", None)

            # Extract Dedalus-specific extensions
            if hasattr(model, "attributes") and model.attributes:
                agent_attributes = agent_attributes if agent_attributes is not None else model.attributes
            if hasattr(model, "metadata") and model.metadata:
                # metadata is stored but not yet fully utilized
                pass

            # Log warnings for unsupported parameters
            unsupported_params = []
            if hasattr(model, "n") and model.n is not None:
                unsupported_params.append("n")
            if hasattr(model, "stop") and model.stop is not None:
                unsupported_params.append("stop")
            if hasattr(model, "stream_options") and model.stream_options is not None:
                unsupported_params.append("stream_options")
            if hasattr(model, "logprobs") and model.logprobs is not None:
                unsupported_params.append("logprobs")
            if hasattr(model, "top_logprobs") and model.top_logprobs is not None:
                unsupported_params.append("top_logprobs")
            if hasattr(model, "seed") and model.seed is not None:
                unsupported_params.append("seed")
            if hasattr(model, "service_tier") and model.service_tier is not None:
                unsupported_params.append("service_tier")
            if hasattr(model, "tools") and model.tools is not None:
                unsupported_params.append("tools")
            if hasattr(model, "parallel_tool_calls") and model.parallel_tool_calls is not None:
                unsupported_params.append("parallel_tool_calls")
            if hasattr(model, "user") and model.user is not None:
                unsupported_params.append("user")
            if hasattr(model, "max_completion_tokens") and model.max_completion_tokens is not None:
                unsupported_params.append("max_completion_tokens")

            if unsupported_params:
                import warnings

                warnings.warn(
                    f"The following DedalusModel parameters are not yet supported and will be ignored: {', '.join(unsupported_params)}. "
                    f"Support for these parameters is coming soon.",
                    UserWarning,
                    stacklevel=2,
                )
        else:  # Single string
            model_name = model
            model_list = [model] if model else []

        available_models = model_list if available_models is None else available_models

        model_config = _ModelConfig(
            id=str(model_name),
            model_list=model_list,  # Pass the full model list
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logit_bias=logit_bias,
            response_format=response_format,
            agent_attributes=agent_attributes,
            model_attributes=model_attributes,
            tool_choice=tool_choice,
            guardrails=guardrails,
            handoff_config=handoff_config,
        )

        # Normalize mcp_servers to list
        normalized_mcp_servers = [mcp_servers] if isinstance(mcp_servers, str) else (mcp_servers or [])

        exec_config = _ExecutionConfig(
            mcp_servers=normalized_mcp_servers,
            max_steps=max_steps,
            stream=stream,
            transport=transport,
            verbose=verbose if verbose is not None else self.verbose,
            debug=debug or False,
            on_tool_event=on_tool_event,
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
                    conversation = [{"role": "system", "content": instructions}, {"role": "user", "content": input}]
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

            response = await self.client.chat.completions.create(
                model=policy_result["model"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

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
            await self._execute_tool_calls(
                tool_calls, tool_handler, messages, tool_results, tools_called, steps, verbose=exec_config.verbose
            )

        return _RunResult(
            final_output=final_text, tool_results=tool_results, steps_used=steps, tools_called=tools_called, messages=messages
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
                stream=True,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

            tool_calls = []
            chunk_count = 0
            content_chunks = 0
            tool_call_chunks = 0
            finish_reason = None
            async for chunk in stream:
                chunk_count += 1
                if exec_config.verbose:
                    # Only surface agent_updated metadata; suppress raw chunk spam
                    extra = getattr(chunk, "__pydantic_extra__", None)
                    if isinstance(extra, dict):
                        meta = extra.get("x_dedalus_event") or extra.get("dedalus_event")
                        if isinstance(meta, dict) and meta.get("type") == "agent_updated":
                            print(f" [EVENT] agent_updated: agent={meta.get('agent')} model={meta.get('model')}")
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

                # When MCP tools are involved and content was streamed, we're done
                if mcp_names and has_streamed_content:
                    if exec_config.verbose:
                        print(f" MCP tools called and content streamed - response complete, breaking loop")
                    break

                if all_mcp:
                    # All tools are MCP - the response should be streamed
                    if exec_config.verbose:
                        print(f" All tools are MCP, expecting streamed response")
                    # Don't break here - let the next iteration handle it
                else:
                    # We have at least one local tool
                    # Filter to only include local tool calls in the assistant message
                    local_only_tool_calls = [
                        tc for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]
                    messages.append({"role": "assistant", "tool_calls": local_only_tool_calls})
                    if exec_config.verbose:
                        print(
                            f" Added assistant message with {len(local_only_tool_calls)} local tool calls (filtered from {len(tool_calls)} total)"
                        )

                    # Execute only local tools
                    for tc in tool_calls:
                        fn_name = tc["function"]["name"]
                        fn_args_str = tc["function"]["arguments"]

                        if fn_name in getattr(tool_handler, "_funcs", {}):
                            # Local tool
                            try:
                                fn_args = json.loads(fn_args_str)
                            except json.JSONDecodeError:
                                fn_args = {}

                            try:
                                result = await tool_handler.exec(fn_name, fn_args)
                                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
                                if exec_config.verbose:
                                    print(f" Executed local tool {fn_name}: {str(result)[:50]}...")
                            except Exception as e:
                                messages.append(
                                    {"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"}
                                )
                                if exec_config.verbose:
                                    print(f" Error executing local tool {fn_name}: {e}")
                        else:
                            # MCP tool - DON'T add any message
                            # The API server should handle this
                            if exec_config.verbose:
                                print(f" MCP tool {fn_name} - skipping (server will handle)")

                    if exec_config.verbose:
                        print(f" Messages after tool execution: {len(messages)}")

                        # Only continue if we have NO MCP tools
                        if not mcp_names:
                            print(f" No MCP tools, continuing loop to step {steps + 1}...")
                        else:
                            print(f" MCP tools present, expecting response in next iteration")

                # Continue loop only if we need another response
                if exec_config.verbose:
                    print(f" Tool processing complete")
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

            response = self.client.chat.completions.create(
                model=policy_result["model"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

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
            self._execute_tool_calls_sync(tool_calls, tool_handler, messages, tool_results, tools_called, steps)

        return _RunResult(
            final_output=final_text, tool_results=tool_results, steps_used=steps, tools_called=tools_called, messages=messages
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
                stream=True,
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

            tool_calls = []
            chunk_count = 0
            content_chunks = 0
            tool_call_chunks = 0
            finish_reason = None
            accumulated_content = ""

            for chunk in stream:
                chunk_count += 1
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
                                if hasattr(tc_delta, 'function') and hasattr(tc_delta.function, 'name') and tc_delta.function.name:
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

                # When MCP tools are involved and content was streamed, we're done
                if mcp_names and has_streamed_content:
                    if exec_config.verbose:
                        print(f"  MCP tools called and content streamed - response complete, breaking loop")
                    break

                if all_mcp:
                    # All tools are MCP - the response should be streamed
                    if exec_config.verbose:
                        print(f"  All tools are MCP, expecting streamed response")
                    # Don't break here - let the next iteration handle it
                else:
                    # We have at least one local tool
                    # Filter to only include local tool calls in the assistant message
                    local_only_tool_calls = [
                        tc for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]
                    messages.append({"role": "assistant", "tool_calls": local_only_tool_calls})
                    if exec_config.verbose:
                        print(
                            f" Added assistant message with {len(local_only_tool_calls)} local tool calls (filtered from {len(tool_calls)} total)"
                        )

                    # Execute only local tools
                    for tc in tool_calls:
                        fn_name = tc["function"]["name"]
                        fn_args_str = tc["function"]["arguments"]

                        if fn_name in getattr(tool_handler, "_funcs", {}):
                            # Local tool
                            try:
                                fn_args = json.loads(fn_args_str)
                            except json.JSONDecodeError:
                                fn_args = {}

                            try:
                                result = tool_handler.exec_sync(fn_name, fn_args)
                                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
                                if exec_config.verbose:
                                    print(f" Executed local tool {fn_name}: {str(result)[:50]}...")
                            except Exception as e:
                                messages.append(
                                    {"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"}
                                )
                                if exec_config.verbose:
                                    print(f" Error executing local tool {fn_name}: {e}")
                        else:
                            # MCP tool - DON'T add any message
                            # The API server should handle this
                            if exec_config.verbose:
                                print(f" MCP tool {fn_name} - skipping (server will handle)")

                    if exec_config.verbose:
                        print(f" Messages after tool execution: {len(messages)}")

                        # Only continue if we have NO MCP tools
                        if not mcp_names:
                            print(f" No MCP tools, continuing loop to step {steps + 1}...")
                        else:
                            print(f" MCP tools present, expecting response in next iteration")

                # Continue loop only if we need another response
                if exec_config.verbose:
                    print(f" Tool processing complete")
            else:
                if exec_config.verbose:
                    print(f" No tool calls found, breaking out of loop")
                break

    def _apply_policy(
        self, policy: PolicyInput, context: PolicyContext, model_config: _ModelConfig, exec_config: _ExecutionConfig
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

            calls.append(
                {
                    "id": tc_dict.get("id", ""),
                    "type": tc_dict.get("type", "function"),
                    "function": {"name": fn_dict.get("name", ""), "arguments": fn_dict.get("arguments", "{}")},
                }
            )
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
        """Execute tool calls asynchronously."""
        if verbose:
            print(f" _execute_tool_calls: Processing {len(tool_calls)} tool calls")

        for i, tc in enumerate(tool_calls):
            fn_name = tc["function"]["name"]
            fn_args_str = tc["function"]["arguments"]

            if verbose:
                print(f" Tool {i + 1}/{len(tool_calls)}: {fn_name}")

            # Always record the assistant tool_call message so subsequent tool responses are valid.
            messages.append({"role": "assistant", "tool_calls": [tc]})

            try:
                fn_args = json.loads(fn_args_str)
            except json.JSONDecodeError:
                fn_args = {}

            try:
                result = await tool_handler.exec(fn_name, fn_args)
                tool_results.append({"name": fn_name, "result": result, "step": step})
                tools_called.append(fn_name)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})

                if verbose:
                    print(f" Tool {fn_name} executed successfully: {str(result)[:50]}...")
            except Exception as e:
                error_result = {"error": str(e), "name": fn_name, "step": step}
                tool_results.append(error_result)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"})

                if verbose:
                    print(f" Tool {fn_name} failed with error: {e}")
                    print(f" Error type: {type(e).__name__}")

    def _execute_tool_calls_sync(
        self,
        tool_calls: list[ToolCall],
        tool_handler: _ToolHandler,
        messages: list[Message],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
    ):
        """Execute tool calls synchronously."""
        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            fn_args_str = tc["function"]["arguments"]

            messages.append({"role": "assistant", "tool_calls": [tc]})

            try:
                fn_args = json.loads(fn_args_str)
            except json.JSONDecodeError:
                fn_args = {}

            try:
                result = tool_handler.exec_sync(fn_name, fn_args)
                tool_results.append({"name": fn_name, "result": result, "step": step})
                tools_called.append(fn_name)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
            except Exception as e:
                error_result = {"error": str(e), "name": fn_name, "step": step}
                tool_results.append(error_result)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"})

    def _accumulate_tool_calls(self, deltas, acc: list[ToolCall]) -> None:
        """Accumulate streaming tool call deltas."""
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

    @staticmethod
    def _mk_kwargs(mc: _ModelConfig) -> Dict[str, Any]:
        """Convert model config to kwargs for client call."""
        from ...lib._parsing import type_to_response_format_param
        from ..._utils import is_given

        d = asdict(mc)
        d.pop("id", None)  # Remove id since it's passed separately
        d.pop("model_list", None)  # Remove model_list since it's not an API parameter

        # Convert Pydantic model to dict schema if needed
        if "response_format" in d and d["response_format"] is not None:
            converted = type_to_response_format_param(d["response_format"])
            d["response_format"] = converted if is_given(converted) else None

        return {k: v for k, v in d.items() if v is not None}
