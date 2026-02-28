# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for MCP request credential embedding."""

from __future__ import annotations

from typing import TypedDict
from dataclasses import dataclass

import pytest

from dedalus_labs.lib.mcp import request as mcp_request
from dedalus_labs.lib.mcp.wire import slug_to_connection_name


@dataclass(frozen=True)
class _FakeConnection:
    name: str


@dataclass(frozen=True)
class _FakeCredential:
    connection: _FakeConnection
    encrypted_blob: str

    def values_for_encryption(self) -> dict[str, str]:
        return {"blob": self.encrypted_blob}


class _RequestPayload(TypedDict):
    mcp_servers: list[str]
    credentials: list[_FakeCredential]


class _FakeHTTPClient:
    pass


class _FakePublicKey:
    pass


def _build_payload() -> _RequestPayload:
    return {
        "mcp_servers": [
            "dedalus-labs/gmail-mcp",
            "dedalus-labs/slack-mcp",
            "dedalus-labs/calendar-mcp",
        ],
        "credentials": [
            _FakeCredential(_FakeConnection("dedalus-labs-gmail-mcp"), "enc-gmail"),
            _FakeCredential(_FakeConnection("dedalus-labs-slack-mcp"), "enc-slack"),
        ],
    }


def _expected_mcp_servers() -> list[dict[str, str | dict[str, str] | None]]:
    return [
        {
            "slug": "dedalus-labs/gmail-mcp",
            "name": "dedalus-labs/gmail-mcp",
            "credentials": {"dedalus-labs-gmail-mcp": "enc-gmail"},
        },
        {
            "slug": "dedalus-labs/slack-mcp",
            "name": "dedalus-labs/slack-mcp",
            "credentials": {"dedalus-labs-slack-mcp": "enc-slack"},
        },
        {
            "slug": "dedalus-labs/calendar-mcp",
            "name": "dedalus-labs/calendar-mcp",
            "credentials": None,
        },
    ]


def _fake_encrypt_credentials(_public_key: _FakePublicKey, values: dict[str, str]) -> str:
    return values["blob"]


class TestSlugToConnectionName:
    def test_slug_to_connection_name(self) -> None:
        assert slug_to_connection_name("dedalus-labs/gmail-mcp") == "dedalus-labs-gmail-mcp"


class TestPrepareMCPRequest:
    def test_sync_embeds_per_server_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def _fake_fetch_sync(_http: _FakeHTTPClient, _url: str) -> _FakePublicKey:
            return _FakePublicKey()

        monkeypatch.setattr(mcp_request, "fetch_encryption_key_sync", _fake_fetch_sync)
        monkeypatch.setattr(mcp_request, "encrypt_credentials", _fake_encrypt_credentials)

        result = mcp_request.prepare_mcp_request_sync(
            _build_payload(),
            "https://auth.example.com",
            _FakeHTTPClient(),
        )

        assert "credentials" not in result
        assert result["mcp_servers"] == _expected_mcp_servers()

    @pytest.mark.asyncio
    async def test_async_embeds_per_server_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        async def _fake_fetch_async(_http: _FakeHTTPClient, _url: str) -> _FakePublicKey:
            return _FakePublicKey()

        monkeypatch.setattr(mcp_request, "fetch_encryption_key", _fake_fetch_async)
        monkeypatch.setattr(mcp_request, "encrypt_credentials", _fake_encrypt_credentials)

        result = await mcp_request.prepare_mcp_request(
            _build_payload(),
            "https://auth.example.com",
            _FakeHTTPClient(),
        )

        assert "credentials" not in result
        assert result["mcp_servers"] == _expected_mcp_servers()
