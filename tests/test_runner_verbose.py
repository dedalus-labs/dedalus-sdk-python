# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Regression tests for verbose-mode logging in DedalusRunner.

Reproduces dedalus-labs/dedalus-sdk-python#54: ``verbose=True`` crashed with an
``AttributeError`` on the first response containing tool calls because the
verbose print path called ``.get(...)`` on SDK model objects (which behave like
attribute-only objects, not dicts).
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from dedalus_labs.lib.runner.core import DedalusRunner, _tool_call_name


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def _model_tool_call(call_id: str, name: str, arguments: str):
    """A tool call shaped like an SDK model object (attribute access, no ``.get``)."""
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=arguments),
    )


def _response_with_tool_calls(*tool_calls):
    message = SimpleNamespace(content=None, tool_calls=list(tool_calls))
    return SimpleNamespace(model="test-model", choices=[SimpleNamespace(message=message)])


def _response_with_text(text: str):
    message = SimpleNamespace(content=text, tool_calls=None)
    return SimpleNamespace(model="test-model", choices=[SimpleNamespace(message=message)])


def test_tool_call_name_accepts_dicts_and_model_objects():
    assert _tool_call_name({"function": {"name": "add"}}) == "add"
    assert _tool_call_name(_model_tool_call("c1", "add", "{}")) == "add"
    assert _tool_call_name({"function": SimpleNamespace(name="add")}) == "add"
    assert _tool_call_name({}) == "?"
    assert _tool_call_name(SimpleNamespace()) == "?"


def test_run_verbose_with_model_tool_calls_does_not_crash(capsys):
    client = MagicMock()
    client.chat.completions.create.side_effect = [
        _response_with_tool_calls(_model_tool_call("call_1", "add", '{"a": 3, "b": 4}')),
        _response_with_text("The sum is 7."),
    ]
    client.mcp_tool_results = None

    runner = DedalusRunner(client, verbose=True)
    result = runner.run(
        model="openai/gpt-test",
        input="What is 3 + 4? You MUST call the add tool.",
        tools=[add],
    )

    assert result.tools_called == ["add"]
    assert result.final_output == "The sum is 7."
    # The verbose path should have printed the tool call name, not "?".
    assert "add" in capsys.readouterr().out
