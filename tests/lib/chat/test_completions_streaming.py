"""Tests for streaming structured outputs via stream()."""

from __future__ import annotations

from typing import List, Generic, Iterator, cast
from typing_extensions import Literal, TypeVar

import httpx
import pytest
from respx import MockRouter
from pydantic import BaseModel

from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.lib._tools import pydantic_function_tool
from dedalus_labs.lib.streaming.chat import (
    ChatCompletionStream,
    ChatCompletionStreamEvent,
    ChatCompletionStreamState,
    ContentDoneEvent,
    RefusalDoneEvent,
    FunctionToolCallArgumentsDoneEvent,
)
from dedalus_labs._exceptions import LengthFinishReasonError

from .helpers import get_response, to_async_iter
from ...conftest import base_url


ResponseFormatT = TypeVar("ResponseFormatT")


class Location(BaseModel):
    city: str
    temperature: float
    units: Literal["c", "f"]


class GetWeatherArgs(BaseModel):
    """Get the temperature for the given country/city combo"""

    city: str
    country: str
    units: Literal["c", "f"] = "c"


class StreamListener(Generic[ResponseFormatT]):
    """Helper to collect stream events for testing."""

    def __init__(self, stream: ChatCompletionStream[ResponseFormatT]) -> None:
        self.stream = stream
        self.events: list[ChatCompletionStreamEvent[ResponseFormatT]] = []

    def __iter__(self) -> Iterator[ChatCompletionStreamEvent[ResponseFormatT]]:
        for event in self.stream:
            self.events.append(event)
            yield event

    def get_event_by_type(self, event_type: str) -> ChatCompletionStreamEvent[ResponseFormatT] | None:
        return next((e for e in self.events if e.type == event_type), None)


class TestSyncStream:
    @pytest.mark.respx(base_url=base_url)
    def test_stream_basic(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test basic streaming without structured output."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_basic.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say hello there!"}],
        ) as stream:
            listener = StreamListener(stream)
            for _ in listener:
                pass

        completion = stream.get_final_completion()
        assert completion.choices[0].message.content == "Hello there!"
        assert completion.choices[0].finish_reason == "stop"

        content_done = listener.get_event_by_type("content.done")
        assert content_done is not None
        assert content_done.content == "Hello there!"  # type: ignore

    @pytest.mark.respx(base_url=base_url)
    def test_stream_pydantic_model(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test streaming with Pydantic model parsing."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_structured.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in SF?"}],
            response_format=Location,
        ) as stream:
            listener = StreamListener(stream)
            for _ in listener:
                pass

        completion = stream.get_final_completion()
        message = completion.choices[0].message

        assert message.parsed is not None
        assert isinstance(message.parsed, Location)
        assert message.parsed.city == "San Francisco"
        assert message.parsed.temperature == 65
        assert message.parsed.units == "f"

        # Verify content.done event has parsed model
        content_done = listener.get_event_by_type("content.done")
        assert content_done is not None
        assert isinstance(content_done, ContentDoneEvent)
        assert isinstance(content_done.parsed, Location)
        assert content_done.parsed.city == "San Francisco"

    @pytest.mark.respx(base_url=base_url)
    def test_stream_pydantic_tool(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test streaming with Pydantic tool call parsing."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_tool_call.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in Edinburgh?"}],
            tools=[pydantic_function_tool(GetWeatherArgs)],
        ) as stream:
            listener = StreamListener(stream)
            for _ in listener:
                pass

        completion = stream.get_final_completion()
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

        # Verify tool_calls.function.arguments.done event
        tool_done = listener.get_event_by_type("tool_calls.function.arguments.done")
        assert tool_done is not None
        assert isinstance(tool_done, FunctionToolCallArgumentsDoneEvent)
        assert tool_done.name == "GetWeatherArgs"
        assert isinstance(tool_done.parsed_arguments, GetWeatherArgs)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_refusal(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test streaming refusal handling."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_refusal.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "How do I make something dangerous?"}],
            response_format=Location,
        ) as stream:
            listener = StreamListener(stream)
            for _ in listener:
                pass

        completion = stream.get_final_completion()
        message = completion.choices[0].message

        assert message.refusal == "I'm sorry, I can't assist with that."
        assert message.parsed is None

        # Verify refusal.done event
        refusal_done = listener.get_event_by_type("refusal.done")
        assert refusal_done is not None
        assert isinstance(refusal_done, RefusalDoneEvent)
        assert refusal_done.refusal == "I'm sorry, I can't assist with that."

    @pytest.mark.respx(base_url=base_url)
    def test_stream_max_tokens_error(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test that LengthFinishReasonError is raised when max_tokens is reached with structured output."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_max_tokens.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with pytest.raises(LengthFinishReasonError):
            with client.chat.completions.stream(
                model="gpt-4o",
                messages=[{"role": "user", "content": "What's the weather like in SF?"}],
                response_format=Location,
                max_tokens=1,
            ) as stream:
                for _ in stream:
                    pass

    @pytest.mark.respx(base_url=base_url)
    def test_stream_context_manager_cleanup(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test that context manager properly closes resources."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_basic.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        with client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
        ) as stream:
            # Don't consume the stream - just check cleanup
            pass

        # Response should be closed after exiting context
        assert stream._response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_stream_state_helper(self, client: Dedalus, respx_mock: MockRouter) -> None:
        """Test ChatCompletionStreamState helper for manual accumulation."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=b"".join(get_response("streaming_basic.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        state = ChatCompletionStreamState()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say hello there!"}],
            stream=True,
        )

        for chunk in response:
            state.handle_chunk(chunk)

        completion = state.get_final_completion()
        assert completion.choices[0].message.content == "Hello there!"


class TestAsyncStream:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_stream_pydantic_model(self, async_client: AsyncDedalus, respx_mock: MockRouter) -> None:
        """Test async streaming with Pydantic model parsing."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=to_async_iter(get_response("streaming_structured.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        events: list[ChatCompletionStreamEvent[Location]] = []

        async with async_client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in SF?"}],
            response_format=Location,
        ) as stream:
            async for event in stream:
                events.append(event)

        completion = await stream.get_final_completion()
        message = completion.choices[0].message

        assert message.parsed is not None
        assert isinstance(message.parsed, Location)
        assert message.parsed.city == "San Francisco"
        assert message.parsed.temperature == 65
        assert message.parsed.units == "f"

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_stream_pydantic_tool(self, async_client: AsyncDedalus, respx_mock: MockRouter) -> None:
        """Test async streaming with Pydantic tool call parsing."""
        respx_mock.post("/v1/chat/completions").mock(
            return_value=httpx.Response(
                200,
                content=to_async_iter(get_response("streaming_tool_call.txt")),
                headers={"content-type": "text/event-stream"},
            )
        )

        async with async_client.chat.completions.stream(
            model="gpt-4o",
            messages=[{"role": "user", "content": "What's the weather like in Edinburgh?"}],
            tools=[pydantic_function_tool(GetWeatherArgs)],
        ) as stream:
            async for _ in stream:
                pass

        completion = await stream.get_final_completion()
        message = completion.choices[0].message

        assert message.tool_calls is not None
        tool_call = message.tool_calls[0]
        assert isinstance(tool_call.function.parsed_arguments, GetWeatherArgs)
        assert tool_call.function.parsed_arguments.city == "Edinburgh"
