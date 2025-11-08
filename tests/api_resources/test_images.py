# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types import ImagesResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_variation(self, client: Dedalus) -> None:
        image = client.images.create_variation(
            image=b"raw file contents",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_variation_with_all_params(self, client: Dedalus) -> None:
        image = client.images.create_variation(
            image=b"raw file contents",
            model="model",
            n=0,
            response_format="response_format",
            size="size",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_variation(self, client: Dedalus) -> None:
        response = client.images.with_raw_response.create_variation(
            image=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_variation(self, client: Dedalus) -> None:
        with client.images.with_streaming_response.create_variation(
            image=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_edit(self, client: Dedalus) -> None:
        image = client.images.edit(
            image=b"raw file contents",
            prompt="prompt",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_edit_with_all_params(self, client: Dedalus) -> None:
        image = client.images.edit(
            image=b"raw file contents",
            prompt="prompt",
            mask=b"raw file contents",
            model="model",
            n=0,
            response_format="response_format",
            size="size",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_edit(self, client: Dedalus) -> None:
        response = client.images.with_raw_response.edit(
            image=b"raw file contents",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_edit(self, client: Dedalus) -> None:
        with client.images.with_streaming_response.edit(
            image=b"raw file contents",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate(self, client: Dedalus) -> None:
        image = client.images.generate(
            prompt="A white siamese cat",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_with_all_params(self, client: Dedalus) -> None:
        image = client.images.generate(
            prompt="A white siamese cat",
            background="transparent",
            model="openai/dall-e-3",
            moderation="auto",
            n=1,
            output_compression=85,
            output_format="png",
            partial_images=0,
            quality="standard",
            response_format="url",
            size="1024x1024",
            stream=True,
            style="vivid",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate(self, client: Dedalus) -> None:
        response = client.images.with_raw_response.generate(
            prompt="A white siamese cat",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate(self, client: Dedalus) -> None:
        with client.images.with_streaming_response.generate(
            prompt="A white siamese cat",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncImages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_variation(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.create_variation(
            image=b"raw file contents",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_variation_with_all_params(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.create_variation(
            image=b"raw file contents",
            model="model",
            n=0,
            response_format="response_format",
            size="size",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_variation(self, async_client: AsyncDedalus) -> None:
        response = await async_client.images.with_raw_response.create_variation(
            image=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_variation(self, async_client: AsyncDedalus) -> None:
        async with async_client.images.with_streaming_response.create_variation(
            image=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_edit(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.edit(
            image=b"raw file contents",
            prompt="prompt",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_edit_with_all_params(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.edit(
            image=b"raw file contents",
            prompt="prompt",
            mask=b"raw file contents",
            model="model",
            n=0,
            response_format="response_format",
            size="size",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_edit(self, async_client: AsyncDedalus) -> None:
        response = await async_client.images.with_raw_response.edit(
            image=b"raw file contents",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_edit(self, async_client: AsyncDedalus) -> None:
        async with async_client.images.with_streaming_response.edit(
            image=b"raw file contents",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.generate(
            prompt="A white siamese cat",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncDedalus) -> None:
        image = await async_client.images.generate(
            prompt="A white siamese cat",
            background="transparent",
            model="openai/dall-e-3",
            moderation="auto",
            n=1,
            output_compression=85,
            output_format="png",
            partial_images=0,
            quality="standard",
            response_format="url",
            size="1024x1024",
            stream=True,
            style="vivid",
            user="user",
        )
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncDedalus) -> None:
        response = await async_client.images.with_raw_response.generate(
            prompt="A white siamese cat",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImagesResponse, image, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncDedalus) -> None:
        async with async_client.images.with_streaming_response.generate(
            prompt="A white siamese cat",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImagesResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True
