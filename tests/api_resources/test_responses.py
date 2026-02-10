# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types import Response

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResponses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Dedalus) -> None:
        response = client.responses.create()
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Dedalus) -> None:
        response = client.responses.create(
            background=True,
            conversation="string",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            frequency_penalty=0,
            include=["message.output_text.logprobs"],
            input="What is the capital of France?",
            instructions="You are a helpful assistant.",
            max_output_tokens=1000,
            max_tool_calls=10,
            mcp_servers="dedalus-labs/example-server",
            metadata={"foo": "string"},
            model="openai/gpt-4o",
            parallel_tool_calls=True,
            presence_penalty=0,
            previous_response_id="previous_response_id",
            prompt={
                "id": "id",
                "variables": {"foo": "string"},
                "version": "version",
            },
            prompt_cache_key="prompt_cache_key",
            reasoning={"foo": "string"},
            safety_identifier="safety_identifier",
            service_tier="auto",
            store=True,
            stream=True,
            stream_options={"foo": "string"},
            temperature=0,
            text={"foo": "string"},
            tool_choice="auto",
            tools=[
                {
                    "function": {
                        "description": None,
                        "name": None,
                        "parameters": None,
                    },
                    "type": "function",
                }
            ],
            top_logprobs=5,
            top_p=0.1,
            truncation="auto",
            user="user",
        )
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Dedalus) -> None:
        http_response = client.responses.with_raw_response.create()

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = http_response.parse()
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Dedalus) -> None:
        with client.responses.with_streaming_response.create() as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = http_response.parse()
            assert_matches_type(Response, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True


class TestAsyncResponses:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncDedalus) -> None:
        response = await async_client.responses.create()
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncDedalus) -> None:
        response = await async_client.responses.create(
            background=True,
            conversation="string",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            frequency_penalty=0,
            include=["message.output_text.logprobs"],
            input="What is the capital of France?",
            instructions="You are a helpful assistant.",
            max_output_tokens=1000,
            max_tool_calls=10,
            mcp_servers="dedalus-labs/example-server",
            metadata={"foo": "string"},
            model="openai/gpt-4o",
            parallel_tool_calls=True,
            presence_penalty=0,
            previous_response_id="previous_response_id",
            prompt={
                "id": "id",
                "variables": {"foo": "string"},
                "version": "version",
            },
            prompt_cache_key="prompt_cache_key",
            reasoning={"foo": "string"},
            safety_identifier="safety_identifier",
            service_tier="auto",
            store=True,
            stream=True,
            stream_options={"foo": "string"},
            temperature=0,
            text={"foo": "string"},
            tool_choice="auto",
            tools=[
                {
                    "function": {
                        "description": None,
                        "name": None,
                        "parameters": None,
                    },
                    "type": "function",
                }
            ],
            top_logprobs=5,
            top_p=0.1,
            truncation="auto",
            user="user",
        )
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncDedalus) -> None:
        http_response = await async_client.responses.with_raw_response.create()

        assert http_response.is_closed is True
        assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"
        response = await http_response.parse()
        assert_matches_type(Response, response, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncDedalus) -> None:
        async with async_client.responses.with_streaming_response.create() as http_response:
            assert not http_response.is_closed
            assert http_response.http_request.headers.get("X-Stainless-Lang") == "python"

            response = await http_response.parse()
            assert_matches_type(Response, response, path=["response"])

        assert cast(Any, http_response.is_closed) is True
