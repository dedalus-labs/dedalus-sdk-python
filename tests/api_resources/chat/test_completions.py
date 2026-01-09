# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types.chat import (
    ChatCompletion,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: Dedalus) -> None:
        completion = client.chat.completions.create(
            model="openai/gpt-5",
        )
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Dedalus) -> None:
        completion = client.chat.completions.create(
            model="openai/gpt-5",
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
            },
            audio={
                "format": "wav",
                "voice": "string",
            },
            automatic_tool_execution=True,
            cached_content="cached_content",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            deferred=True,
            frequency_penalty=-2,
            function_call="function_call",
            functions=[
                {
                    "name": "name",
                    "description": "description",
                    "parameters": {"foo": "string"},
                }
            ],
            generation_config={"foo": "string"},
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=1,
            max_turns=5,
            mcp_servers="dedalus-labs/example-server",
            messages=[
                {
                    "content": "string",
                    "role": "developer",
                    "name": "name",
                }
            ],
            metadata={"foo": "string"},
            modalities=["string"],
            model_attributes={
                "gpt-5": {
                    "accuracy": 0.95,
                    "speed": 0.6,
                }
            },
            n=1,
            parallel_tool_calls=True,
            prediction={
                "content": "string",
                "type": "content",
            },
            presence_penalty=-2,
            prompt_cache_key="prompt_cache_key",
            prompt_cache_retention="prompt_cache_retention",
            prompt_mode="reasoning",
            reasoning_effort="reasoning_effort",
            response_format={"type": "text"},
            safe_prompt=True,
            safety_identifier="safety_identifier",
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_UNSPECIFIED",
                    "threshold": "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
                }
            ],
            search_parameters={"foo": "string"},
            seed=0,
            service_tier="service_tier",
            stop=["string"],
            store=True,
            stream=False,
            stream_options={"foo": "string"},
            system_instruction={"foo": "string"},
            temperature=0,
            thinking={
                "budget_tokens": 1024,
                "type": "enabled",
            },
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tool_config={"foo": "string"},
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {"foo": "string"},
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
            verbosity="verbosity",
            web_search_options={"foo": "string"},
        )
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: Dedalus) -> None:
        response = client.chat.completions.with_raw_response.create(
            model="openai/gpt-5",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Dedalus) -> None:
        with client.chat.completions.with_streaming_response.create(
            model="openai/gpt-5",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = response.parse()
            assert_matches_type(ChatCompletion, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: Dedalus) -> None:
        completion_stream = client.chat.completions.create(
            model="openai/gpt-5",
            stream=True,
        )
        completion_stream.response.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Dedalus) -> None:
        completion_stream = client.chat.completions.create(
            model="openai/gpt-5",
            stream=True,
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
            },
            audio={
                "format": "wav",
                "voice": "string",
            },
            automatic_tool_execution=True,
            cached_content="cached_content",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            deferred=True,
            frequency_penalty=-2,
            function_call="function_call",
            functions=[
                {
                    "name": "name",
                    "description": "description",
                    "parameters": {"foo": "string"},
                }
            ],
            generation_config={"foo": "string"},
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=1,
            max_turns=5,
            mcp_servers="dedalus-labs/example-server",
            messages=[
                {
                    "content": "string",
                    "role": "developer",
                    "name": "name",
                }
            ],
            metadata={"foo": "string"},
            modalities=["string"],
            model_attributes={
                "gpt-5": {
                    "accuracy": 0.95,
                    "speed": 0.6,
                }
            },
            n=1,
            parallel_tool_calls=True,
            prediction={
                "content": "string",
                "type": "content",
            },
            presence_penalty=-2,
            prompt_cache_key="prompt_cache_key",
            prompt_cache_retention="prompt_cache_retention",
            prompt_mode="reasoning",
            reasoning_effort="reasoning_effort",
            response_format={"type": "text"},
            safe_prompt=True,
            safety_identifier="safety_identifier",
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_UNSPECIFIED",
                    "threshold": "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
                }
            ],
            search_parameters={"foo": "string"},
            seed=0,
            service_tier="service_tier",
            stop=["string"],
            store=True,
            stream_options={"foo": "string"},
            system_instruction={"foo": "string"},
            temperature=0,
            thinking={
                "budget_tokens": 1024,
                "type": "enabled",
            },
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tool_config={"foo": "string"},
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {"foo": "string"},
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
            verbosity="verbosity",
            web_search_options={"foo": "string"},
        )
        completion_stream.response.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: Dedalus) -> None:
        response = client.chat.completions.with_raw_response.create(
            model="openai/gpt-5",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Dedalus) -> None:
        with client.chat.completions.with_streaming_response.create(
            model="openai/gpt-5",
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
            model="openai/gpt-5",
        )
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncDedalus) -> None:
        completion = await async_client.chat.completions.create(
            model="openai/gpt-5",
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
            },
            audio={
                "format": "wav",
                "voice": "string",
            },
            automatic_tool_execution=True,
            cached_content="cached_content",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            deferred=True,
            frequency_penalty=-2,
            function_call="function_call",
            functions=[
                {
                    "name": "name",
                    "description": "description",
                    "parameters": {"foo": "string"},
                }
            ],
            generation_config={"foo": "string"},
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=1,
            max_turns=5,
            mcp_servers="dedalus-labs/example-server",
            messages=[
                {
                    "content": "string",
                    "role": "developer",
                    "name": "name",
                }
            ],
            metadata={"foo": "string"},
            modalities=["string"],
            model_attributes={
                "gpt-5": {
                    "accuracy": 0.95,
                    "speed": 0.6,
                }
            },
            n=1,
            parallel_tool_calls=True,
            prediction={
                "content": "string",
                "type": "content",
            },
            presence_penalty=-2,
            prompt_cache_key="prompt_cache_key",
            prompt_cache_retention="prompt_cache_retention",
            prompt_mode="reasoning",
            reasoning_effort="reasoning_effort",
            response_format={"type": "text"},
            safe_prompt=True,
            safety_identifier="safety_identifier",
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_UNSPECIFIED",
                    "threshold": "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
                }
            ],
            search_parameters={"foo": "string"},
            seed=0,
            service_tier="service_tier",
            stop=["string"],
            store=True,
            stream=False,
            stream_options={"foo": "string"},
            system_instruction={"foo": "string"},
            temperature=0,
            thinking={
                "budget_tokens": 1024,
                "type": "enabled",
            },
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tool_config={"foo": "string"},
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {"foo": "string"},
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
            verbosity="verbosity",
            web_search_options={"foo": "string"},
        )
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.completions.with_raw_response.create(
            model="openai/gpt-5",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = await response.parse()
        assert_matches_type(ChatCompletion, completion, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.completions.with_streaming_response.create(
            model="openai/gpt-5",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = await response.parse()
            assert_matches_type(ChatCompletion, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncDedalus) -> None:
        completion_stream = await async_client.chat.completions.create(
            model="openai/gpt-5",
            stream=True,
        )
        await completion_stream.response.aclose()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncDedalus) -> None:
        completion_stream = await async_client.chat.completions.create(
            model="openai/gpt-5",
            stream=True,
            agent_attributes={
                "accuracy": 0.9,
                "complexity": 0.8,
            },
            audio={
                "format": "wav",
                "voice": "string",
            },
            automatic_tool_execution=True,
            cached_content="cached_content",
            credentials={
                "connection_name": "external-service",
                "values": {"api_key": "sk-..."},
            },
            deferred=True,
            frequency_penalty=-2,
            function_call="function_call",
            functions=[
                {
                    "name": "name",
                    "description": "description",
                    "parameters": {"foo": "string"},
                }
            ],
            generation_config={"foo": "string"},
            guardrails=[{"foo": "bar"}],
            handoff_config={"foo": "bar"},
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=1,
            max_turns=5,
            mcp_servers="dedalus-labs/example-server",
            messages=[
                {
                    "content": "string",
                    "role": "developer",
                    "name": "name",
                }
            ],
            metadata={"foo": "string"},
            modalities=["string"],
            model_attributes={
                "gpt-5": {
                    "accuracy": 0.95,
                    "speed": 0.6,
                }
            },
            n=1,
            parallel_tool_calls=True,
            prediction={
                "content": "string",
                "type": "content",
            },
            presence_penalty=-2,
            prompt_cache_key="prompt_cache_key",
            prompt_cache_retention="prompt_cache_retention",
            prompt_mode="reasoning",
            reasoning_effort="reasoning_effort",
            response_format={"type": "text"},
            safe_prompt=True,
            safety_identifier="safety_identifier",
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_UNSPECIFIED",
                    "threshold": "HARM_BLOCK_THRESHOLD_UNSPECIFIED",
                }
            ],
            search_parameters={"foo": "string"},
            seed=0,
            service_tier="service_tier",
            stop=["string"],
            store=True,
            stream_options={"foo": "string"},
            system_instruction={"foo": "string"},
            temperature=0,
            thinking={
                "budget_tokens": 1024,
                "type": "enabled",
            },
            tool_choice={
                "type": "auto",
                "disable_parallel_tool_use": True,
            },
            tool_config={"foo": "string"},
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {"foo": "string"},
                        "strict": True,
                    },
                    "type": "function",
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
            verbosity="verbosity",
            web_search_options={"foo": "string"},
        )
        await completion_stream.response.aclose()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        response = await async_client.chat.completions.with_raw_response.create(
            model="openai/gpt-5",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncDedalus) -> None:
        async with async_client.chat.completions.with_streaming_response.create(
            model="openai/gpt-5",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
