# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dedalus_labs import Dedalus, AsyncDedalus
from dedalus_labs.types import OCRResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOCR:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_process(self, client: Dedalus) -> None:
        ocr = client.ocr.process(
            document={"document_url": "document_url"},
        )
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_process_with_all_params(self, client: Dedalus) -> None:
        ocr = client.ocr.process(
            document={
                "document_url": "document_url",
                "type": "type",
            },
            model="model",
        )
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_process(self, client: Dedalus) -> None:
        response = client.ocr.with_raw_response.process(
            document={"document_url": "document_url"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ocr = response.parse()
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_process(self, client: Dedalus) -> None:
        with client.ocr.with_streaming_response.process(
            document={"document_url": "document_url"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ocr = response.parse()
            assert_matches_type(OCRResponse, ocr, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOCR:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_process(self, async_client: AsyncDedalus) -> None:
        ocr = await async_client.ocr.process(
            document={"document_url": "document_url"},
        )
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncDedalus) -> None:
        ocr = await async_client.ocr.process(
            document={
                "document_url": "document_url",
                "type": "type",
            },
            model="model",
        )
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_process(self, async_client: AsyncDedalus) -> None:
        response = await async_client.ocr.with_raw_response.process(
            document={"document_url": "document_url"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ocr = await response.parse()
        assert_matches_type(OCRResponse, ocr, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncDedalus) -> None:
        async with async_client.ocr.with_streaming_response.process(
            document={"document_url": "document_url"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ocr = await response.parse()
            assert_matches_type(OCRResponse, ocr, path=["response"])

        assert cast(Any, response.is_closed) is True
