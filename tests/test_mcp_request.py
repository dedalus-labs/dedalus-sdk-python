# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for MCP request credential embedding."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from dedalus_labs.lib.mcp import request as mcp_request
from dedalus_labs.lib.mcp.wire import slug_to_connection_name


def _fake_encrypted_credentials() -> mcp_request.EncryptedCredentials:
    return mcp_request.EncryptedCredentials(
        **{
            "dedalus-labs-gmail-mcp": "enc-gmail",
            "dedalus-labs-slack-mcp": "enc-slack",
        }
    )


class TestSlugToConnectionName:
    def test_slug_to_connection_name(self) -> None:
        assert slug_to_connection_name("dedalus-labs/gmail-mcp") == "dedalus-labs-gmail-mcp"


class TestPrepareMCPRequest:
    def test_sync_embeds_per_server_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(mcp_request, "fetch_encryption_key_sync", lambda _http, _url: object())
        monkeypatch.setattr(mcp_request, "_encrypt_credentials", lambda _creds, _key: _fake_encrypted_credentials())

        data: Dict[str, Any] = {
            "mcp_servers": [
                "dedalus-labs/gmail-mcp",
                "dedalus-labs/slack-mcp",
                "dedalus-labs/calendar-mcp",
            ],
            "credentials": [object(), object()],
        }

        result = mcp_request.prepare_mcp_request_sync(data, "https://auth.example.com", object())

        assert "credentials" not in result
        assert result["mcp_servers"] == [
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

    @pytest.mark.asyncio
    async def test_async_embeds_per_server_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        async def fake_fetch(_http: Any, _url: str) -> object:
            return object()

        monkeypatch.setattr(mcp_request, "fetch_encryption_key", fake_fetch)
        monkeypatch.setattr(mcp_request, "_encrypt_credentials", lambda _creds, _key: _fake_encrypted_credentials())

        data: Dict[str, Any] = {
            "mcp_servers": [
                "dedalus-labs/gmail-mcp",
                "dedalus-labs/slack-mcp",
                "dedalus-labs/calendar-mcp",
            ],
            "credentials": [object(), object()],
        }

        result = await mcp_request.prepare_mcp_request(data, "https://auth.example.com", object())

        assert "credentials" not in result
        assert result["mcp_servers"] == [
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
