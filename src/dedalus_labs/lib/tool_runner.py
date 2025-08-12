"""Clean, streamlined tool runner for executing tools locally."""

import asyncio
import inspect
import json
from typing import Any, Callable, Optional

from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.lib.to_schema import to_schema


class Runner:
    """Tool runner for client-side execution."""

    def __init__(self, client: Dedalus | AsyncDedalus, *, verbose: bool = False) -> None:
        self.client = client
        self.verbose = verbose
        self._is_async = isinstance(client, AsyncDedalus)
        self._reset_state()

    def _reset_state(self):
        """Reset internal state for new run."""
        self.conversation_history = []
        self.tool_results = []
        self._tool_registry = {}
        self._turns_used = 0
    
    def run(self, *args, **kwargs):
        """Run method that delegates to sync or async implementation based on client type."""
        if self._is_async:
            # Return the coroutine for async usage
            return self._run_async(*args, **kwargs)
        else:
            # Execute synchronously
            return self._run_sync(*args, **kwargs)

    async def _run_async(
        self,
        input: str,
        tools: list[Callable | str],
        model: str,
        mcp_servers: list[str] | None = None,
        max_turns: int = 10,
        *,
        json_mode: bool = False,
        verbose: bool | None = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute tools with automatic conversation management.

        Returns dict with final_output, turns_used, and tools_executed.
        In json_mode, returns raw response data instead.
        """
        self._reset_state()
        self.verbose = verbose if verbose is not None else self.verbose

        # Setup tools
        local_tools, mcp_slugs = self._categorize_tools(tools)
        self._build_registry(tools)

        # Check if streaming is requested
        if stream:
            # For streaming, we need to return the stream object directly
            # The user will handle streaming and tool execution manually
            return await self._call_api(
                messages=[{"role": "user", "content": input}],
                tools=self._convert_to_schemas(local_tools),
                mcp_servers=(mcp_servers or []) + mcp_slugs,
                model=model,
                stream=True,
                **kwargs,
            )
        
        # Non-streaming: handle tool execution automatically
        response = await self._call_api(
            messages=[{"role": "user", "content": input}],
            tools=self._convert_to_schemas(local_tools),
            mcp_servers=(mcp_servers or []) + mcp_slugs,
            model=model,
            **kwargs,
        )

        # Execute tool loop
        final_output = await self._execute_loop(
            response, max_turns, model, tools, mcp_servers
        )

        # Return appropriate format
        if json_mode:
            return self._format_json_response(response)

        return {
            "final_output": final_output,
            "turns_used": self._turns_used,
            "tools_executed": [r["tool"] for r in self.tool_results],
        }
    
    def _run_sync(
        self,
        input: str,
        tools: list[Callable | str],
        model: str,
        mcp_servers: list[str] | None = None,
        max_turns: int = 10,
        *,
        json_mode: bool = False,
        verbose: bool | None = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Synchronous version of run for sync clients."""
        self._reset_state()
        self.verbose = verbose if verbose is not None else self.verbose

        # Setup tools
        local_tools, mcp_slugs = self._categorize_tools(tools)
        self._build_registry(tools)

        # Check if streaming is requested
        if stream:
            # For streaming, return the stream object directly
            return self._call_api_sync(
                messages=[{"role": "user", "content": input}],
                tools=self._convert_to_schemas(local_tools),
                mcp_servers=(mcp_servers or []) + mcp_slugs,
                model=model,
                stream=True,
                **kwargs,
            )
        
        # Non-streaming: handle tool execution automatically
        response = self._call_api_sync(
            messages=[{"role": "user", "content": input}],
            tools=self._convert_to_schemas(local_tools),
            mcp_servers=(mcp_servers or []) + mcp_slugs,
            model=model,
            **kwargs,
        )

        # Execute tool loop (sync)
        final_output = self._execute_loop_sync(
            response, max_turns, model, tools, mcp_servers
        )

        # Return appropriate format
        if json_mode:
            return self._format_json_response(response)

        return {
            "final_output": final_output,
            "turns_used": self._turns_used,
            "tools_executed": [r["tool"] for r in self.tool_results],
        }

    def _categorize_tools(self, tools: list[Callable | str]) -> tuple:
        """Split tools into local functions and MCP server strings."""
        local_tools = [t for t in tools if callable(t)]
        mcp_slugs = [t for t in tools if isinstance(t, str)]
        return local_tools, mcp_slugs

    # TODO: Type annotatoin
    def _build_registry(self, tools: list[Callable | str]):
        """Build tool name -> function mapping."""
        for tool in tools:
            if callable(tool):
                name = getattr(tool, '__name__', None)
                if name is None:
                    msg = f"Cannot infer name for callable tool: {tool}"
                    raise ValueError(msg)
                self._tool_registry[name] = tool

            elif isinstance(tool, str):
                self._tool_registry[tool] = f"mcp_server:{tool}"

    def _convert_to_schemas(self, tools: list[Callable]) -> list[dict[str, Any]]:
        """Convert functions to OpenAI tool schemas."""
        schemas = []
        for tool in tools:
            schema = to_schema(tool)
            # to_schema already returns the full OpenAI tool schema format
            schemas.append(schema)
        return schemas

    async def _call_api(self, messages: list[dict], **kwargs: Any) -> Any:
        """Make API call and track conversation."""
        if self._is_async:
            response = await self.client.chat.create(input=messages, **kwargs)
        else:
            response = self.client.chat.create(input=messages, **kwargs)

        # Track conversation
        if messages and messages[-1]["role"] == "user":
            self.conversation_history.extend(messages)

        if hasattr(response, "choices") and response.choices:
            msg = response.choices[0].message
            self.conversation_history.append({"role": msg.role, "content": msg.content})

        return response
    
    def _call_api_sync(self, messages: list[dict], **kwargs: Any) -> Any:
        """Synchronous API call for sync clients."""
        response = self.client.chat.create(input=messages, **kwargs)

        # Track conversation
        if messages and messages[-1]["role"] == "user":
            self.conversation_history.extend(messages)

        if hasattr(response, "choices") and response.choices:
            msg = response.choices[0].message
            self.conversation_history.append({"role": msg.role, "content": msg.content})

        return response

    async def _execute_loop(
        self,
        initial_response: Any,
        max_turns: int,
        model: str,
        tools: list[Callable | str],
        mcp_servers: list[str] | None,
    ) -> str:
        """Execute tool calls until completion or max turns."""
        response = initial_response

        for turn in range(max_turns):
            self._turns_used = turn + 1

            # Extract content
            content = response.choices[0].message.content if response.choices else ""
            
            # Parse metadata from content for MCP tools
            if "<!-- DEDALUS_METADATA:" in content:
                import re
                metadata_match = re.search(r'<!-- DEDALUS_METADATA: executed_tools=([^>]+) -->', content)
                if metadata_match:
                    executed_tools = metadata_match.group(1).split(',')
                    for tool in executed_tools:
                        self.tool_results.append({
                            "tool": tool.strip(),
                            "result": "[MCP server-side execution]",
                            "error": False
                        })
                    # Remove metadata from content for cleaner output
                    content = re.sub(r'\n*<!-- DEDALUS_METADATA:[^>]+-->', '', content)
                    # Update response content if we modified it
                    if response.choices:
                        response.choices[0].message.content = content
            
            # Check if response has tool_calls attribute
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                # Process tool calls from the message object
                for tool_call in response.choices[0].message.tool_calls:
                    self.tool_results.append({
                        "tool": tool_call.function.name,
                        "result": "[Executed by API]",
                        "error": False
                    })

            # Check for tool calls in content (legacy)
            if not self._has_tool_calls(content):
                return content

            # Parse and execute
            tool_calls = self._parse_tool_calls(content)
            if not tool_calls:
                return content

            # Execute tools
            results = await self._execute_tools(tool_calls)
            if not results:
                return content

            # Continue conversation
            self.conversation_history.append(
                {"role": "user", "content": self._format_results(results)}
            )
            
            # Track MCP tools that were called but not executed locally
            for tc in tool_calls:
                tool_name = tc["name"]
                if tool_name not in self._tool_registry or \
                   (isinstance(self._tool_registry.get(tool_name), str) and 
                    self._tool_registry[tool_name].startswith("mcp_server:")):
                    # This is an MCP tool - track it
                    self.tool_results.append({"tool": tool_name, "result": "[MCP server-side]", "error": False})

            # Next API call
            local_tools, mcp_slugs = self._categorize_tools(tools)
            response = await self._call_api(
                messages=self.conversation_history,
                model=model,
                tools=self._convert_to_schemas(local_tools),
                mcp_servers=(mcp_servers or []) + mcp_slugs,
            )

        return (
            response.choices[0].message.content
            if response.choices
            else "Max turns reached"
        )
    
    def _execute_loop_sync(
        self,
        initial_response: Any,
        max_turns: int,
        model: str,
        tools: list[Callable | str],
        mcp_servers: list[str] | None,
    ) -> str:
        """Synchronous version of execute loop."""
        response = initial_response

        for turn in range(max_turns):
            self._turns_used = turn + 1

            # Extract content
            content = response.choices[0].message.content if response.choices else ""
            
            # Parse metadata from content for MCP tools
            if "<!-- DEDALUS_METADATA:" in content:
                import re
                metadata_match = re.search(r'<!-- DEDALUS_METADATA: executed_tools=([^>]+) -->', content)
                if metadata_match:
                    executed_tools = metadata_match.group(1).split(',')
                    for tool in executed_tools:
                        self.tool_results.append({
                            "tool": tool.strip(),
                            "result": "[MCP server-side execution]",
                            "error": False
                        })
                    # Remove metadata from content for cleaner output
                    content = re.sub(r'\n*<!-- DEDALUS_METADATA:[^>]+-->', '', content)
                    # Update response content if we modified it
                    if response.choices:
                        response.choices[0].message.content = content
            
            # Check if response has tool_calls attribute
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                # Process tool calls from the message object
                for tool_call in response.choices[0].message.tool_calls:
                    self.tool_results.append({
                        "tool": tool_call.function.name,
                        "result": "[Executed by API]",
                        "error": False
                    })

            # Check for tool calls in content (legacy)
            if not self._has_tool_calls(content):
                return content

            # Parse and execute
            tool_calls = self._parse_tool_calls(content)
            if not tool_calls:
                return content

            # Execute tools synchronously
            results = self._execute_tools_sync(tool_calls)
            if not results:
                return content

            # Continue conversation
            self.conversation_history.append(
                {"role": "user", "content": self._format_results(results)}
            )
            
            # Track MCP tools that were called but not executed locally
            for tc in tool_calls:
                tool_name = tc["name"]
                if tool_name not in self._tool_registry or \
                   (isinstance(self._tool_registry.get(tool_name), str) and 
                    self._tool_registry[tool_name].startswith("mcp_server:")):
                    # This is an MCP tool - track it
                    self.tool_results.append({"tool": tool_name, "result": "[MCP server-side]", "error": False})

            # Next API call
            local_tools, mcp_slugs = self._categorize_tools(tools)
            response = self._call_api_sync(
                messages=self.conversation_history,
                model=model,
                tools=self._convert_to_schemas(local_tools),
                mcp_servers=(mcp_servers or []) + mcp_slugs,
            )

        return (
            response.choices[0].message.content
            if response.choices
            else "Max turns reached"
        )

    def _has_tool_calls(self, content: str) -> bool:
        """Check if response contains tool calls."""
        if self.verbose:
            print(f"[DEBUG] Checking for tool calls in content: {content[:200]}...")
        return "ModelResponse(" in content and "ResponseFunctionToolCall" in content

    def _parse_tool_calls(self, content: str) -> list[dict[str, Any]]:
        """Extract tool calls from response."""
        import re

        pattern = r"ResponseFunctionToolCall\(arguments='([^']*)', call_id='([^']*)', name='([^']*)', type='function_call'"
        matches = re.findall(pattern, content)

        return [
            {"id": call_id, "name": name, "arguments": arguments}
            for arguments, call_id, name in matches
        ]

    async def _execute_tools(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Execute tool calls, filtering out MCP server tools."""
        tasks = []

        for tc in tool_calls:
            tool_name = tc["name"]

            # Skip MCP server tools (executed server-side)
            if tool_name not in self._tool_registry:
                continue

            tool = self._tool_registry[tool_name]
            if isinstance(tool, str) and tool.startswith("mcp_server:"):
                continue

            # Execute local tool
            tasks.append(self._execute_single_tool(tc, tool))

        if not tasks:
            return []

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, dict)]
    
    def _execute_tools_sync(
        self, tool_calls: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Synchronous version of execute tools."""
        results = []

        for tc in tool_calls:
            tool_name = tc["name"]

            # Skip MCP server tools (executed server-side)
            if tool_name not in self._tool_registry:
                continue

            tool = self._tool_registry[tool_name]
            if isinstance(tool, str) and tool.startswith("mcp_server:"):
                continue

            # Execute local tool
            result = self._execute_single_tool_sync(tc, tool)
            if result:
                results.append(result)

        return results

    async def _execute_single_tool(
        self, tool_call: dict[str, Any], func: Callable
    ) -> dict[str, Any]:
        """Execute a single tool and return result."""
        tool_name = tool_call["name"]

        try:
            args = json.loads(tool_call["arguments"])

            if self.verbose:
                print(f"[TOOL CALL] {tool_name}({tool_call['arguments']})")

            # Execute
            if inspect.iscoroutinefunction(func):
                result = await func(**args)
            else:
                result = func(**args)

            tool_result = {"tool": tool_name, "result": str(result), "error": False}
            self.tool_results.append(tool_result)
            return tool_result

        except Exception as e:
            error_result = {
                "tool": tool_name,
                "result": f"Error: {str(e)}",
                "error": True,
            }
            self.tool_results.append(error_result)
            return error_result
    
    def _execute_single_tool_sync(
        self, tool_call: dict[str, Any], func: Callable
    ) -> dict[str, Any]:
        """Synchronous version of execute single tool."""
        tool_name = tool_call["name"]

        try:
            args = json.loads(tool_call["arguments"])

            if self.verbose:
                print(f"[TOOL CALL] {tool_name}({tool_call['arguments']})")

            # Execute (sync functions only)
            if inspect.iscoroutinefunction(func):
                # Run async function in sync context
                result = asyncio.get_event_loop().run_until_complete(func(**args))
            else:
                result = func(**args)

            tool_result = {"tool": tool_name, "result": str(result), "error": False}
            self.tool_results.append(tool_result)
            return tool_result

        except Exception as e:
            error_result = {
                "tool": tool_name,
                "result": f"Error: {str(e)}",
                "error": True,
            }
            self.tool_results.append(error_result)
            return error_result

    def _format_results(self, results: list[dict[str, Any]]) -> str:
        """Format tool results for conversation."""
        if not results:
            return "Tool execution completed"

        parts = [f"{r['tool']}: {r['result']}" for r in results]
        return f"Tool execution results: {'; '.join(parts)}"

    def _format_json_response(self, response: Any) -> dict[str, Any]:
        """Format response for json_mode."""
        return {
            "raw_response": response.model_dump()
            if hasattr(response, "model_dump")
            else dict(response),
            "tool_results": self.tool_results,
            "conversation_history": self.conversation_history,
        }