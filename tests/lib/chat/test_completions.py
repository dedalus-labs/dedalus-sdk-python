"""Tests for non-streaming structured outputs via parse()."""

from __future__ import annotations

import json
from typing import List
from typing_extensions import Literal

import httpx
import pytest
from respx import MockRouter
from pydantic import BaseModel

from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.lib._tools import pydantic_function_tool
from dedalus_labs.types.chat.parsed_chat_completion import (
    ParsedChatCompletion,
    ParsedChoice,
    ParsedChatCompletionMessage,
)

from ...conftest import base_url


class Location(BaseModel):
    city: str
    temperature: float
    units: Literal["c", "f"]


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]


class GetWeatherArgs(BaseModel):
    """Get the temperature for the given country/city combo"""

    city: str
    country: str
    units: Literal["c", "f"] = "c"


def make_completion_response(
    content: str | None = None,
    refusal: str | None = None,
    tool_calls: list | None = None,
    finish_reason: str = "stop",
) -> dict:
    """Create a mock chat completion response."""
    message: dict = {"role": "assistant"}
    if content is not None:
        message["content"] = content
    if refusal is not None:
        message["refusal"] = refusal
    if tool_calls is not None:
        message["tool_calls"] = tool_calls

    return {
        "id": "chatcmpl-test123",
        "object": "chat.completion",
        "created": 1727346143,
        "model": "gpt-4o",
        "choices": [
            {
                "index": 0,
                "message": message,
                "logprobs": None,
                "finish_reason": finish_reason,
            }
        ],
        "usage": {
            "prompt_tokens": 79,
            "completion_tokens": 14,
            "total_tokens": 93,
        },
        "system_fingerprint": "fp_test",
    }


class TestSyncParse:
    @pytest.mark.respx(base_url=base_url)
    def test_parse_pydantic_model(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test parsing a response into a Pydantic model."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content='{"city":"San Francisco","temperature":65,"units":"f"}'
                ),
            )
        )

        completion = client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in SF?"}],
            response_format=Location,
        )

        assert isinstance(completion, ParsedChatCompletion)
        assert len(completion.choices) == 1

        message = completion.choices[0].message
        assert message.parsed is not None
        assert isinstance(message.parsed, Location)
        assert message.parsed.city == "San Francisco"
        assert message.parsed.temperature == 65.0
        assert message.parsed.units == "f"

    @pytest.mark.respx(base_url=base_url)
    def test_parse_pydantic_model_with_list(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test parsing a response with a list field."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content='{"name":"Science Fair","date":"Friday","participants":["Alice","Bob"]}'
                ),
            )
        )

        completion = client.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Extract the event information."},
                {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
            ],
            response_format=CalendarEvent,
        )

        assert completion.choices[0].message.parsed is not None
        parsed = completion.choices[0].message.parsed
        assert isinstance(parsed, CalendarEvent)
        assert parsed.name == "Science Fair"
        assert parsed.date == "Friday"
        assert parsed.participants == ["Alice", "Bob"]

    @pytest.mark.respx(base_url=base_url)
    def test_parse_without_response_format(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test parse() without a response_format returns parsed=None."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(content="Hello! How can I help you today?"),
            )
        )

        completion = client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
        )

        assert completion.choices[0].message.content == "Hello! How can I help you today?"
        assert completion.choices[0].message.parsed is None

    @pytest.mark.respx(base_url=base_url)
    def test_parse_refusal(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test handling of model refusals."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content=None, refusal="I'm sorry, I can't assist with that."
                ),
            )
        )

        completion = client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "How do I make something dangerous?"}],
            response_format=Location,
        )

        message = completion.choices[0].message
        assert message.refusal == "I'm sorry, I can't assist with that."
        assert message.parsed is None
        assert message.content is None

    @pytest.mark.respx(base_url=base_url)
    def test_parse_pydantic_tool(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test parsing tool calls with Pydantic models."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content=None,
                    tool_calls=[
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "GetWeatherArgs",
                                "arguments": '{"city":"Edinburgh","country":"UK","units":"c"}',
                            },
                        }
                    ],
                    finish_reason="tool_calls",
                ),
            )
        )

        completion = client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in Edinburgh?"}],
            tools=[pydantic_function_tool(GetWeatherArgs)],
        )

        message = completion.choices[0].message
        assert message.tool_calls is not None
        assert len(message.tool_calls) == 1

        tool_call = message.tool_calls[0]
        assert tool_call.function.name == "GetWeatherArgs"
        assert tool_call.function.parsed_arguments is not None
        assert isinstance(tool_call.function.parsed_arguments, GetWeatherArgs)
        assert tool_call.function.parsed_arguments.city == "Edinburgh"
        assert tool_call.function.parsed_arguments.country == "UK"
        assert tool_call.function.parsed_arguments.units == "c"


class TestAsyncParse:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_parse_pydantic_model(self, async_client: AsyncDedalus, respx_mock: MockRouter) -> None:
        """Test async parsing a response into a Pydantic model."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content='{"city":"San Francisco","temperature":65,"units":"f"}'
                ),
            )
        )

        completion = await async_client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in SF?"}],
            response_format=Location,
        )

        assert isinstance(completion, ParsedChatCompletion)
        message = completion.choices[0].message
        assert message.parsed is not None
        assert isinstance(message.parsed, Location)
        assert message.parsed.city == "San Francisco"

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_parse_pydantic_tool(self, async_client: AsyncDedalus, respx_mock: MockRouter) -> None:
        """Test async parsing tool calls with Pydantic models."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                json=make_completion_response(
                    content=None,
                    tool_calls=[
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "GetWeatherArgs",
                                "arguments": '{"city":"Edinburgh","country":"UK","units":"c"}',
                            },
                        }
                    ],
                    finish_reason="tool_calls",
                ),
            )
        )

        completion = await async_client.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in Edinburgh?"}],
            tools=[pydantic_function_tool(GetWeatherArgs)],
        )

        message = completion.choices[0].message
        assert message.tool_calls is not None
        tool_call = message.tool_calls[0]
        assert isinstance(tool_call.function.parsed_arguments, GetWeatherArgs)
        assert tool_call.function.parsed_arguments.city == "Edinburgh"
