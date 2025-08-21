# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types.chat import StreamChunk

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: Dedalus) -> None:
        completion = client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        )
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Dedalus) -> None:
        completion = client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            model="openai/gpt-4",
            model_attributes={
                "anthropic/claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "openai/gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "openai/gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            stream=False,
            temperature=0,
            tool_choice="auto",
            tools=[
                {
                    "function": "bar",
                    "type": "bar",
                }
            ],
            top_p=0.1,
            user="user-123",
        )
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: Dedalus) -> None:
        response = client.chat.completions.with_raw_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Dedalus) -> None:
        with client.chat.completions.with_streaming_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = response.parse()
            assert_matches_type(StreamChunk, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: Dedalus) -> None:
        completion_stream = client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        )
        completion_stream.response.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Dedalus) -> None:
        completion_stream = client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            model="openai/gpt-4",
            model_attributes={
                "anthropic/claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "openai/gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "openai/gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            temperature=0,
            tool_choice="auto",
            tools=[
                {
                    "function": "bar",
                    "type": "bar",
                }
            ],
            top_p=0.1,
            user="user-123",
        )
        completion_stream.response.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: Dedalus) -> None:
        response = client.chat.completions.with_raw_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Dedalus) -> None:
        with client.chat.completions.with_streaming_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncCompletions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncDedalus) -> None:
        completion = await async_client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        )
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncDedalus) -> None:
        completion = await async_client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            model="openai/gpt-4",
            model_attributes={
                "anthropic/claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "openai/gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "openai/gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            stream=False,
            temperature=0,
            tool_choice="auto",
            tools=[
                {
                    "function": "bar",
                    "type": "bar",
                }
            ],
            top_p=0.1,
            user="user-123",
        )
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.completions.with_raw_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = await response.parse()
        assert_matches_type(StreamChunk, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.completions.with_streaming_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = await response.parse()
            assert_matches_type(StreamChunk, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncDedalus) -> None:
        completion_stream = await async_client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        )
        await completion_stream.response.aclose()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncDedalus) -> None:
        completion_stream = await async_client.chat.completions.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            model="openai/gpt-4",
            model_attributes={
                "anthropic/claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "openai/gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "openai/gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            temperature=0,
            tool_choice="auto",
            tools=[
                {
                    "function": "bar",
                    "type": "bar",
                }
            ],
            top_p=0.1,
            user="user-123",
        )
        await completion_stream.response.aclose()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.completions.with_raw_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.completions.with_streaming_response.create(
            messages=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
