# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

import asyncio
import inspect
import json
from typing import Any, Callable, Iterator, Protocol, Literal, AsyncIterator
from dataclasses import dataclass, asdict, field

from pydantic import create_model
from dedalus_labs import Dedalus, AsyncDedalus
from .runner_types import SchemaProcessingError

import logging
logger = logging.getLogger(__name__)

# Message and tool types (no external dependencies)
MessageDict = dict[str, str | list[dict[str, str]]]  # role, content, tool_calls with string values
ToolCall = dict[str, str | dict[str, str]]  # id, type, function: {name, arguments}
ToolResult = dict[str, str | float | bool | None]  # tool execution result
PolicyContext = dict[str, int | list[MessageDict] | str | list[str]]  # step, messages, model, etc
JsonValue = (
    str | int | float | bool | None | dict[str, str | int | float] | list[str | int | float]
)  # JSON-serializable but narrowed

# Policy processing types
PolicyInput = Callable[[PolicyContext], dict[str, JsonValue]] | dict[str, JsonValue] | None


def _process_policy(policy: PolicyInput, context: PolicyContext) -> dict[str, JsonValue]:
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


def to_schema(func: Callable) -> dict[str, JsonValue]:
    """Convert a Python function's signature to an OpenAPI-compatible JSON schema using Pydantic."""
    try:
        sig = inspect.signature(func)
        fields: dict[str, Any] = {}

        for name, param in sig.parameters.items():
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else str
            default = param.default if param.default != inspect.Parameter.empty else ...
            fields[name] = (annotation, default)

        if not fields:
            fields["input"] = (str, ...)

        DynamicModel = create_model(func.__name__, **fields)
        schema = DynamicModel.model_json_schema()

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or f"Execute {func.__name__}",
                "parameters": schema,
            },
        }
    except Exception:
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": func.__doc__ or f"Execute {func.__name__}",
                "parameters": {"type": "object", "properties": {}},
            },
        }


class _ToolHandler(Protocol):
    def schemas(self) -> list[dict]: ...
    async def exec(self, name: str, args: dict[str, JsonValue]) -> JsonValue: ...


class _FunctionToolHandler:
    """Converts Python functions to tool handler via introspection."""

    def __init__(self, funcs: list[Callable]):
        self._funcs = {f.__name__: f for f in funcs}

    def schemas(self) -> list[dict]:
        """Build OpenAI-compatible function schemas via introspection."""
        out: list[dict[str, Any]] = []
        for fn in self._funcs.values():
            try:
                out.append(to_schema(fn))
            except Exception:
                continue
        return out

    async def exec(self, name: str, args: dict[str, JsonValue]) -> JsonValue:
        """Execute tool by name with given args (async)."""
        fn = self._funcs[name]
        if inspect.iscoroutinefunction(fn):
            return await fn(**args)
        return await asyncio.to_thread(fn, **args)

    def exec_sync(self, name: str, args: dict[str, JsonValue]) -> JsonValue:
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
    temperature: float | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    logit_bias: dict[str, int] | None = None
    agent_attributes: dict[str, float] | None = None
    model_attributes: dict[str, dict[str, float]] | None = None
    tool_choice: str | dict[str, JsonValue] | None = None
    guardrails: list[dict[str, JsonValue]] | None = None
    handoff_config: dict[str, JsonValue] | None = None


@dataclass
class _ExecutionConfig:
    """Configuration for tool execution behavior and policies."""

    mcp_servers: list[str] = field(default_factory=list)
    max_steps: int = 10
    stream: bool = False
    transport: Literal["http", "realtime"] = "http"
    verbose: bool = False
    debug: bool = False
    on_tool_event: Callable[[dict[str, JsonValue]], None] | None = None
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
    intents: list[dict[str, JsonValue]] | None = None
    tools_called: list[str] = field(default_factory=list)

    @property
    def output(self) -> str:
        """Legacy compatibility."""
        return self.final_output

    @property
    def content(self) -> str:
        """Legacy compatibility."""
        return self.final_output


class Runner:
    """Unified tool execution runner supporting async/sync and streaming/non-streaming."""

    def __init__(self, client: Dedalus | AsyncDedalus, verbose: bool = False):
        self.client = client
        self.verbose = verbose

    def run(
        self,
        input: str,
        tools: list[Callable] | None = None,
        model: str | list[str] | None = None,
        max_steps: int = 10,
        mcp_servers: list[str] | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        frequency_penalty: float | None = None,
        presence_penalty: float | None = None,
        logit_bias: dict[str, int] | None = None,
        stream: bool = False,
        transport: Literal["http", "realtime"] = "http",
        verbose: bool | None = None,
        debug: bool | None = None,
        on_tool_event: Callable[[dict[str, JsonValue]], None] | None = None,
        return_intent: bool = False,
        agent_attributes: dict[str, float] | None = None,
        model_attributes: dict[str, dict[str, float]] | None = None,
        tool_choice: str | dict[str, JsonValue] | None = None,
        guardrails: list[dict[str, JsonValue]] | None = None,
        handoff_config: dict[str, JsonValue] | None = None,
        policy: PolicyInput = None,
        available_models: list[str] | None = None,
        strict_models: bool = True,
    ):
        """Execute tools with unified async/sync + streaming/non-streaming logic."""
        if not model:
            raise ValueError("model must be provided")

        # Parse model list to get primary and available models
        if isinstance(model, list):
            if not model:
                raise ValueError("model list cannot be empty")
            primary_model = model[0]
            available_models = model
        else:
            primary_model = model
            available_models = [model] if available_models is None else available_models

        model_config = _ModelConfig(
            id=str(primary_model),
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

        exec_config = _ExecutionConfig(
            mcp_servers=mcp_servers or [],
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

        return self._execute_conversation(input, tool_handler, model_config, exec_config)

    def _execute_conversation(
        self, input_text: str, tool_handler: _ToolHandler, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ):
        """Execute conversation with unified logic for all client/streaming combinations."""
        is_async = isinstance(self.client, AsyncDedalus)

        if is_async:
            if exec_config.stream:
                return self._execute_streaming_async(input_text, tool_handler, model_config, exec_config)
            else:
                return self._execute_turns_async(input_text, tool_handler, model_config, exec_config)
        else:
            if exec_config.stream:
                return self._execute_streaming_sync(input_text, tool_handler, model_config, exec_config)
            else:
                return self._execute_turns_sync(input_text, tool_handler, model_config, exec_config)

    async def _execute_turns_async(
        self, input_text: str, tool_handler: _ToolHandler, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ) -> _RunResult:
        """Execute async non-streaming conversation."""
        messages: list[MessageDict] = [{"role": "user", "content": input_text}]
        steps = 0
        final_text = ""
        tool_results: list[ToolResult] = []
        tools_called: list[str] = []

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"\n[RUNNER] Step={steps}")

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
                model=policy_result["model_id"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )
            
            if exec_config.verbose:
                print(f"[DEBUG] Non-streaming response received")
                print(f"[DEBUG] Response type: {type(response)}")

            # Check if we have tool calls
            if not hasattr(response, "choices") or not response.choices:
                final_text = ""
                break

            message = response.choices[0].message
            msg = vars(message) if hasattr(message, '__dict__') else message
            tool_calls = msg.get("tool_calls")
            content = msg.get("content", "")
            
            if exec_config.verbose:
                print(f"[DEBUG] Response content: {content[:100] if content else '(none)'}...")
                if tool_calls:
                    print(f"[DEBUG] Tool calls in response: {[tc.get('function', {}).get('name', '?') for tc in tool_calls]}")

            if not tool_calls:
                final_text = content or ""
                break

            # Execute tools
            tool_calls = self._extract_tool_calls(response.choices[0])
            if exec_config.verbose:
                print(f"[DEBUG] Extracted {len(tool_calls)} tool calls")
                for tc in tool_calls:
                    print(f"  - {tc.get('function', {}).get('name', '?')} (id: {tc.get('id', '?')})")
            await self._execute_tool_calls(tool_calls, tool_handler, messages, tool_results, tools_called, steps, verbose=exec_config.verbose)

        return _RunResult(
            final_output=final_text, tool_results=tool_results, steps_used=steps, tools_called=tools_called
        )

    async def _execute_streaming_async(
        self, input_text: str, tool_handler: _ToolHandler, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ) -> AsyncIterator[Any]:
        """Execute async streaming conversation."""
        messages: list[MessageDict] = [{"role": "user", "content": input_text}]
        steps = 0

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"\n[RUNNER] Step={steps} (max_steps={exec_config.max_steps})")
                print(f"[DEBUG] Starting step {steps} with {len(messages)} messages in conversation")
                print(f"[DEBUG] Message history:")
                for i, msg in enumerate(messages):
                    role = msg.get('role')
                    content = str(msg.get('content', ''))[:50] + '...' if msg.get('content') else ''
                    tool_info = ''
                    if msg.get('tool_calls'):
                        tool_names = [tc.get('function', {}).get('name', '?') for tc in msg.get('tool_calls', [])]
                        tool_info = f" [calling: {', '.join(tool_names)}]"
                    elif msg.get('tool_call_id'):
                        tool_info = f" [response to: {msg.get('tool_call_id')[:8]}...]"
                    print(f"  [{i}] {role}: {content}{tool_info}")

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
                print(f"[DEBUG] Messages being sent to API:")
                for i, msg in enumerate(current_messages):
                    content_preview = str(msg.get('content', ''))[:100]
                    tool_call_info = ""
                    if msg.get('tool_calls'):
                        tool_names = [tc.get('function', {}).get('name', 'unknown') for tc in msg.get('tool_calls', [])]
                        tool_call_info = f" tool_calls=[{', '.join(tool_names)}]"
                    print(f"  [{i}] {msg.get('role')}: {content_preview}...{tool_call_info}")
                print(f"[DEBUG] MCP servers: {policy_result['mcp_servers']}")
                print(f"[DEBUG] Local tools available: {list(getattr(tool_handler, '_funcs', {}).keys())}")

            stream = await self.client.chat.completions.create(
                model=policy_result["model_id"],
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
                    print(f"[DEBUG] Chunk {chunk_count} raw: {chunk}")
                if hasattr(chunk, "choices") and chunk.choices:
                    choice = chunk.choices[0]
                    delta = choice.delta
                    
                    # Check finish reason
                    if hasattr(choice, "finish_reason") and choice.finish_reason:
                        finish_reason = choice.finish_reason
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: finish_reason = {finish_reason}")
                    
                    # Check for tool calls
                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        tool_call_chunks += 1
                        self._accumulate_tool_calls(delta.tool_calls, tool_calls)
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Tool call delta: {delta.tool_calls}")
                    
                    # Check for content
                    if hasattr(delta, "content") and delta.content:
                        content_chunks += 1
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Content: '{delta.content}'")
                    
                    # Check for role
                    if hasattr(delta, "role") and delta.role:
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Role: {delta.role}")
                    
                    yield chunk
            
            if exec_config.verbose:
                print(f"[DEBUG] Stream ended:")
                print(f"  - Total chunks: {chunk_count}")
                print(f"  - Content chunks: {content_chunks}")
                print(f"  - Tool call chunks: {tool_call_chunks}")
                print(f"  - Final finish_reason: {finish_reason}")
                print(f"[DEBUG] Tool calls accumulated: {len(tool_calls)}")
                for tc in tool_calls:
                    print(f"  - {tc.get('function', {}).get('name', 'unknown')} (id: {tc.get('id', 'unknown')})")

            # Execute any accumulated tool calls
            if tool_calls:
                if exec_config.verbose:
                    print(f"[DEBUG] Processing {len(tool_calls)} tool calls")
                
                # Categorize tools
                local_names = [tc["function"]["name"] for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})]
                mcp_names = [tc["function"]["name"] for tc in tool_calls if tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})]
                
                # Check if ALL tools are MCP tools (none are local)
                all_mcp = all(
                    tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})
                    for tc in tool_calls
                )
                
                # Check if stream already contains content (MCP results)
                has_streamed_content = content_chunks > 0
                
                if exec_config.verbose:
                    print(f"[DEBUG] Local tools: {local_names}")
                    print(f"[DEBUG] MCP tools: {mcp_names}") 
                    print(f"[DEBUG] All MCP? {all_mcp}")
                    print(f"[DEBUG] Stream had content? {has_streamed_content} (content_chunks={content_chunks})")
                
                # When MCP tools are involved and content was streamed, we're done
                if mcp_names and has_streamed_content:
                    if exec_config.verbose:
                        print(f"[DEBUG] MCP tools called and content streamed - response complete, breaking loop")
                    break
                
                if all_mcp:
                    # All tools are MCP - the response should be streamed
                    if exec_config.verbose:
                        print(f"[DEBUG] All tools are MCP, expecting streamed response")
                    # Don't break here - let the next iteration handle it
                else:
                    # We have at least one local tool
                    # Filter to only include local tool calls in the assistant message
                    local_only_tool_calls = [
                        tc for tc in tool_calls 
                        if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]
                    messages.append({"role": "assistant", "tool_calls": local_only_tool_calls})
                    if exec_config.verbose:
                        print(f"[DEBUG] Added assistant message with {len(local_only_tool_calls)} local tool calls (filtered from {len(tool_calls)} total)")
                    
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
                                    print(f"[DEBUG] Executed local tool {fn_name}: {str(result)[:50]}...")
                            except Exception as e:
                                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"})
                                if exec_config.verbose:
                                    print(f"[DEBUG] Error executing local tool {fn_name}: {e}")
                        else:
                            # MCP tool - DON'T add any message
                            # The API server should handle this
                            if exec_config.verbose:
                                print(f"[DEBUG] MCP tool {fn_name} - skipping (server will handle)")
                    
                    if exec_config.verbose:
                        print(f"[DEBUG] Messages after tool execution: {len(messages)}")
                        
                        # Only continue if we have NO MCP tools
                        if not mcp_names:
                            print(f"[DEBUG] No MCP tools, continuing loop to step {steps + 1}...")
                        else:
                            print(f"[DEBUG] MCP tools present, expecting response in next iteration")
                
                # Continue loop only if we need another response
                if exec_config.verbose:
                    print(f"[DEBUG] Tool processing complete")
            else:
                if exec_config.verbose:
                    print(f"[DEBUG] No tool calls found, breaking out of loop")
                break
        
        if exec_config.verbose:
            print(f"\n[DEBUG] Exited main loop after {steps} steps")

    def _execute_turns_sync(
        self, input_text: str, tool_handler: _ToolHandler, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ) -> _RunResult:
        """Execute sync non-streaming conversation."""
        messages: list[MessageDict] = [{"role": "user", "content": input_text}]
        steps = 0
        final_text = ""
        tool_results: list[ToolResult] = []
        tools_called: list[str] = []

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"\n[RUNNER] Step={steps}")

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

            response = self.client.chat.completions.create(
                model=policy_result["model_id"],
                messages=current_messages,
                tools=tool_handler.schemas() or None,
                mcp_servers=policy_result["mcp_servers"],
                **{**self._mk_kwargs(model_config), **policy_result["model_kwargs"]},
            )

            # Check if we have tool calls
            if not hasattr(response, "choices") or not response.choices:
                final_text = ""
                break

            message = response.choices[0].message
            msg = vars(message) if hasattr(message, '__dict__') else message
            tool_calls = msg.get("tool_calls")
            content = msg.get("content", "")

            if not tool_calls:
                final_text = content or ""
                break

            # Execute tools
            tool_calls = self._extract_tool_calls(response.choices[0])
            self._execute_tool_calls_sync(tool_calls, tool_handler, messages, tool_results, tools_called, steps)

        return _RunResult(
            final_output=final_text, tool_results=tool_results, steps_used=steps, tools_called=tools_called
        )

    def _execute_streaming_sync(
        self, input_text: str, tool_handler: _ToolHandler, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ) -> Iterator[Any]:
        """Execute sync streaming conversation."""
        messages: list[MessageDict] = [{"role": "user", "content": input_text}]
        steps = 0

        while steps < exec_config.max_steps:
            steps += 1
            if exec_config.verbose:
                print(f"\n[RUNNER] Step={steps} (max_steps={exec_config.max_steps})")
                print(f"[DEBUG] Starting step {steps} with {len(messages)} messages in conversation")
                print(f"[DEBUG] Message history:")
                for i, msg in enumerate(messages):
                    role = msg.get('role')
                    content = str(msg.get('content', ''))[:50] + '...' if msg.get('content') else ''
                    tool_info = ''
                    if msg.get('tool_calls'):
                        tool_names = [tc.get('function', {}).get('name', '?') for tc in msg.get('tool_calls', [])]
                        tool_info = f" [calling: {', '.join(tool_names)}]"
                    elif msg.get('tool_call_id'):
                        tool_info = f" [response to: {msg.get('tool_call_id')[:8]}...]"
                    print(f"  [{i}] {role}: {content}{tool_info}")

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
                print(f"[DEBUG] Messages being sent to API:")
                for i, msg in enumerate(current_messages):
                    content_preview = str(msg.get('content', ''))[:100]
                    tool_call_info = ""
                    if msg.get('tool_calls'):
                        tool_names = [tc.get('function', {}).get('name', 'unknown') for tc in msg.get('tool_calls', [])]
                        tool_call_info = f" tool_calls=[{', '.join(tool_names)}]"
                    print(f"  [{i}] {msg.get('role')}: {content_preview}...{tool_call_info}")
                print(f"[DEBUG] MCP servers: {policy_result['mcp_servers']}")
                print(f"[DEBUG] Local tools available: {list(getattr(tool_handler, '_funcs', {}).keys())}")

            stream = self.client.chat.completions.create(
                model=policy_result["model_id"],
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
            for chunk in stream:
                chunk_count += 1
                if exec_config.verbose:
                    print(f"[DEBUG] Chunk {chunk_count} raw: {chunk}")
                if hasattr(chunk, "choices") and chunk.choices:
                    choice = chunk.choices[0]
                    delta = choice.delta
                    
                    # Check finish reason
                    if hasattr(choice, "finish_reason") and choice.finish_reason:
                        finish_reason = choice.finish_reason
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: finish_reason = {finish_reason}")
                    
                    # Check for tool calls
                    if hasattr(delta, "tool_calls") and delta.tool_calls:
                        tool_call_chunks += 1
                        self._accumulate_tool_calls(delta.tool_calls, tool_calls)
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Tool call delta: {delta.tool_calls}")
                    
                    # Check for content
                    if hasattr(delta, "content") and delta.content:
                        content_chunks += 1
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Content: '{delta.content}'")
                    
                    # Check for role
                    if hasattr(delta, "role") and delta.role:
                        if exec_config.verbose:
                            print(f"[DEBUG] Chunk {chunk_count}: Role: {delta.role}")
                    
                    yield chunk
            
            if exec_config.verbose:
                print(f"[DEBUG] Stream ended:")
                print(f"  - Total chunks: {chunk_count}")
                print(f"  - Content chunks: {content_chunks}")
                print(f"  - Tool call chunks: {tool_call_chunks}")
                print(f"  - Final finish_reason: {finish_reason}")
                print(f"[DEBUG] Tool calls accumulated: {len(tool_calls)}")
                for tc in tool_calls:
                    print(f"  - {tc.get('function', {}).get('name', 'unknown')} (id: {tc.get('id', 'unknown')})")
            
            # Execute any accumulated tool calls
            if tool_calls:
                if exec_config.verbose:
                    print(f"[DEBUG] Processing {len(tool_calls)} tool calls")
                
                # Categorize tools
                local_names = [tc["function"]["name"] for tc in tool_calls if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})]
                mcp_names = [tc["function"]["name"] for tc in tool_calls if tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})]
                
                # Check if ALL tools are MCP tools (none are local)
                all_mcp = all(
                    tc["function"]["name"] not in getattr(tool_handler, "_funcs", {})
                    for tc in tool_calls
                )
                
                # Check if stream already contains content (MCP results)
                has_streamed_content = content_chunks > 0
                
                if exec_config.verbose:
                    print(f"[DEBUG] Local tools: {local_names}")
                    print(f"[DEBUG] MCP tools: {mcp_names}")
                    print(f"[DEBUG] All MCP? {all_mcp}")
                    print(f"[DEBUG] Stream had content? {has_streamed_content} (content_chunks={content_chunks})")
                
                # When MCP tools are involved and content was streamed, we're done
                if mcp_names and has_streamed_content:
                    if exec_config.verbose:
                        print(f"[DEBUG] MCP tools called and content streamed - response complete, breaking loop")
                    break
                
                if all_mcp:
                    # All tools are MCP - the response should be streamed
                    if exec_config.verbose:
                        print(f"[DEBUG] All tools are MCP, expecting streamed response")
                    # Don't break here - let the next iteration handle it
                else:
                    # We have at least one local tool
                    # Filter to only include local tool calls in the assistant message
                    local_only_tool_calls = [
                        tc for tc in tool_calls 
                        if tc["function"]["name"] in getattr(tool_handler, "_funcs", {})
                    ]
                    messages.append({"role": "assistant", "tool_calls": local_only_tool_calls})
                    if exec_config.verbose:
                        print(f"[DEBUG] Added assistant message with {len(local_only_tool_calls)} local tool calls (filtered from {len(tool_calls)} total)")
                    
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
                                    print(f"[DEBUG] Executed local tool {fn_name}: {str(result)[:50]}...")
                            except Exception as e:
                                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"})
                                if exec_config.verbose:
                                    print(f"[DEBUG] Error executing local tool {fn_name}: {e}")
                        else:
                            # MCP tool - DON'T add any message
                            # The API server should handle this
                            if exec_config.verbose:
                                print(f"[DEBUG] MCP tool {fn_name} - skipping (server will handle)")
                    
                    if exec_config.verbose:
                        print(f"[DEBUG] Messages after tool execution: {len(messages)}")
                        
                        # Only continue if we have NO MCP tools
                        if not mcp_names:
                            print(f"[DEBUG] No MCP tools, continuing loop to step {steps + 1}...")
                        else:
                            print(f"[DEBUG] MCP tools present, expecting response in next iteration")
                
                # Continue loop only if we need another response
                if exec_config.verbose:
                    print(f"[DEBUG] Tool processing complete")
            else:
                if exec_config.verbose:
                    print(f"[DEBUG] No tool calls found, breaking out of loop")
                break
        
        if exec_config.verbose:
            print(f"\n[DEBUG] Exited main loop after {steps} steps")

    def _apply_policy(
        self, policy: PolicyInput, context: PolicyContext, model_config: _ModelConfig, exec_config: _ExecutionConfig
    ) -> dict[str, Any]:
        """Apply policy and return unified configuration."""
        pol = _process_policy(policy, context)

        # Start with defaults
        result = {
            "model_id": model_config.id,
            "mcp_servers": list(exec_config.mcp_servers),
            "model_kwargs": {},
            "prepend": [],
            "append": [],
        }

        if pol:
            # Handle model override
            requested_model = pol.get("model")
            if requested_model and exec_config.strict_models and exec_config.available_models:
                if requested_model not in exec_config.available_models:
                    if exec_config.verbose:
                        print(f"[RUNNER] Policy requested unavailable model '{requested_model}', ignoring")
                else:
                    result["model_id"] = str(requested_model)
            elif requested_model:
                result["model_id"] = str(requested_model)

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

    def _build_messages(
        self, messages: list[MessageDict], prepend: list[MessageDict], append: list[MessageDict]
    ) -> list[MessageDict]:
        """Build final message list with prepend/append."""
        return (prepend + messages + append) if (prepend or append) else messages

    def _extract_tool_calls(self, choice) -> list[ToolCall]:
        """Extract tool calls from response choice."""
        if not hasattr(choice, "message"):
            return []
            
        message = choice.message
        msg = vars(message) if hasattr(message, '__dict__') else message
        tool_calls = msg.get("tool_calls", [])
            
        if not tool_calls:
            return []

        calls = []
        for tc in tool_calls:
            tc_dict = vars(tc) if hasattr(tc, '__dict__') else tc
            fn = tc_dict.get("function", {})
            fn_dict = vars(fn) if hasattr(fn, '__dict__') else fn
            
            calls.append({
                "id": tc_dict.get("id", ""),
                "type": tc_dict.get("type", "function"),
                "function": {
                    "name": fn_dict.get("name", ""), 
                    "arguments": fn_dict.get("arguments", "{}")
                },
            })
        return calls

    async def _execute_tool_calls(
        self,
        tool_calls: list[ToolCall],
        tool_handler: _ToolHandler,
        messages: list[MessageDict],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
        verbose: bool = False,
    ):
        """Execute tool calls asynchronously."""
        if verbose:
            print(f"[DEBUG] _execute_tool_calls: Processing {len(tool_calls)} tool calls")
        
        for i, tc in enumerate(tool_calls):
            fn_name = tc["function"]["name"]
            fn_args_str = tc["function"]["arguments"]
            
            if verbose:
                print(f"[DEBUG] Tool {i+1}/{len(tool_calls)}: {fn_name}")

            try:
                fn_args = json.loads(fn_args_str)
            except json.JSONDecodeError:
                fn_args = {}

            try:
                result = await tool_handler.exec(fn_name, fn_args)
                tool_results.append({"name": fn_name, "result": result, "step": step})
                tools_called.append(fn_name)

                # Add tool call and result to conversation
                messages.append({"role": "assistant", "tool_calls": [tc]})
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": str(result)})
                
                if verbose:
                    print(f"[DEBUG] Tool {fn_name} executed successfully: {str(result)[:50]}...")
            except Exception as e:
                error_result = {"error": str(e), "name": fn_name, "step": step}
                tool_results.append(error_result)
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": f"Error: {str(e)}"})
                
                if verbose:
                    print(f"[DEBUG] Tool {fn_name} failed with error: {e}")
                    print(f"[DEBUG] Error type: {type(e).__name__}")

    def _execute_tool_calls_sync(
        self,
        tool_calls: list[ToolCall],
        tool_handler: _ToolHandler,
        messages: list[MessageDict],
        tool_results: list[ToolResult],
        tools_called: list[str],
        step: int,
    ):
        """Execute tool calls synchronously."""
        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            fn_args_str = tc["function"]["arguments"]

            try:
                fn_args = json.loads(fn_args_str)
            except json.JSONDecodeError:
                fn_args = {}

            try:
                result = tool_handler.exec_sync(fn_name, fn_args)
                tool_results.append({"name": fn_name, "result": result, "step": step})
                tools_called.append(fn_name)

                # Add tool call and result to conversation
                messages.append({"role": "assistant", "tool_calls": [tc]})
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
    def _mk_kwargs(mc: _ModelConfig) -> dict[str, Any]:
        """Convert model config to kwargs for client call."""
        d = asdict(mc)
        d.pop("id", None)  # Remove id since it's passed separately
        return {k: v for k, v in d.items() if v is not None}