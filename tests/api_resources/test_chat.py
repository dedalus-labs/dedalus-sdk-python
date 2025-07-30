# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dedalus_sdk import DedalusSDK, AsyncDedalusSDK
from tests.utils import assert_matches_type
from dedalus_sdk.types import ChatCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: DedalusSDK) -> None:
        chat = client.chat.create()
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: DedalusSDK) -> None:
        chat = client.chat.create(
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            input=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            messages=[{"foo": "bar"}],
            model="gpt-4",
            model_attributes={
                "claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            stream=True,
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
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: DedalusSDK) -> None:
        response = client.chat.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: DedalusSDK) -> None:
        with client.chat.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatCreateResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncDedalusSDK) -> None:
        chat = await async_client.chat.create()
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncDedalusSDK) -> None:
        chat = await async_client.chat.create(
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
                "efficiency": 0.7,
            },
            frequency_penalty=-0.5,
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            input=[
                {
                    "content": "bar",
                    "role": "bar",
                }
            ],
            logit_bias={"50256": -100},
            max_tokens=100,
            max_turns=5,
            mcp_servers=["dedalus-labs/brave-search", "dedalus-labs/github-api"],
            messages=[{"foo": "bar"}],
            model="gpt-4",
            model_attributes={
                "claude-3-5-sonnet": {
                    "cost": 0.7,
                    "creativity": 0.8,
                    "intelligence": 0.95,
                },
                "gpt-4": {
                    "cost": 0.8,
                    "intelligence": 0.9,
                    "speed": 0.6,
                },
                "gpt-4o-mini": {
                    "cost": 0.2,
                    "intelligence": 0.7,
                    "speed": 0.9,
                },
            },
            n=1,
            presence_penalty=-0.5,
            stop=["\\n", "END"],
            stream=True,
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
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncDedalusSDK) -> None:
        response = await async_client.chat.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatCreateResponse, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncDedalusSDK) -> None:
        async with async_client.chat.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatCreateResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True
