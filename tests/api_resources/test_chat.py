# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types import Completion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_overload_1(self, client: Dedalus) -> None:
        chat = client.chat.create()
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Dedalus) -> None:
        chat = client.chat.create(
            agent_attributes={"foo": 0},
            frequency_penalty=-2,
            input=[{}],
            logit_bias={"foo": 0},
            max_tokens=1,
            max_turns=1,
            mcp_servers=["string"],
            model="string",
            model_attributes={"foo": {"foo": 0}},
            n=1,
            presence_penalty=-2,
            stop=["string"],
            stream=False,
            temperature=0,
            tool_choice="string",
            tools=[{}],
            top_p=0,
            user="user",
        )
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_overload_1(self, client: Dedalus) -> None:
        response = client.chat.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Dedalus) -> None:
        with client.chat.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(Completion, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_overload_2(self, client: Dedalus) -> None:
        chat_stream = client.chat.create(
            stream=True,
        )
        chat_stream.response.close()

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Dedalus) -> None:
        chat_stream = client.chat.create(
            stream=True,
            agent_attributes={"foo": 0},
            frequency_penalty=-2,
            input=[{}],
            logit_bias={"foo": 0},
            max_tokens=1,
            max_turns=1,
            mcp_servers=["string"],
            model="string",
            model_attributes={"foo": {"foo": 0}},
            n=1,
            presence_penalty=-2,
            stop=["string"],
            temperature=0,
            tool_choice="string",
            tools=[{}],
            top_p=0,
            user="user",
        )
        chat_stream.response.close()

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_overload_2(self, client: Dedalus) -> None:
        response = client.chat.with_raw_response.create(
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Dedalus) -> None:
        with client.chat.with_streaming_response.create(
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncDedalus) -> None:
        chat = await async_client.chat.create()
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncDedalus) -> None:
        chat = await async_client.chat.create(
            agent_attributes={"foo": 0},
            frequency_penalty=-2,
            input=[{}],
            logit_bias={"foo": 0},
            max_tokens=1,
            max_turns=1,
            mcp_servers=["string"],
            model="string",
            model_attributes={"foo": {"foo": 0}},
            n=1,
            presence_penalty=-2,
            stop=["string"],
            stream=False,
            temperature=0,
            tool_choice="string",
            tools=[{}],
            top_p=0,
            user="user",
        )
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(Completion, chat, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(Completion, chat, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncDedalus) -> None:
        chat_stream = await async_client.chat.create(
            stream=True,
        )
        await chat_stream.response.aclose()

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncDedalus) -> None:
        chat_stream = await async_client.chat.create(
            stream=True,
            agent_attributes={"foo": 0},
            frequency_penalty=-2,
            input=[{}],
            logit_bias={"foo": 0},
            max_tokens=1,
            max_turns=1,
            mcp_servers=["string"],
            model="string",
            model_attributes={"foo": {"foo": 0}},
            n=1,
            presence_penalty=-2,
            stop=["string"],
            temperature=0,
            tool_choice="string",
            tools=[{}],
            top_p=0,
            user="user",
        )
        await chat_stream.response.aclose()

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.with_raw_response.create(
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.with_streaming_response.create(
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
