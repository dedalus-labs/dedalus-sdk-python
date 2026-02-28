# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for MCP server wire format serialization."""

from __future__ import annotations

import json
from typing import Any

import pytest
from pydantic import ValidationError

from dedalus_labs.lib.mcp import (
    MCPServerProtocol,
    MCPServerWireSpec,
    is_mcp_server,
    serialize_mcp_servers,
)

# --- Test helpers ---


class FakeMCPServer:
    """Minimal implementation satisfying MCPServerProtocol."""

    def __init__(self, name: str, url: str | None = None) -> None:
        self._name = name
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str | None:
        return self._url

    def serve(self, *args: Any, **kwargs: Any) -> None:
        pass


class IncompleteServer:
    """Missing required protocol attributes."""

    def __init__(self) -> None:
        self.name = "incomplete"


# --- MCPServerWireSpec construction ---


def test_from_slug_simple():
    spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server")
    assert spec.slug == "dedalus-labs/example-server"
    assert spec.version is None


def test_from_slug_with_version():
    spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server", version="v1.2.0")
    assert spec.version == "v1.2.0"


def test_from_slug_with_embedded_version():
    spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server@v2")
    assert spec.slug == "dedalus-labs/example-server"
    assert spec.version == "v2"


def test_from_url():
    spec = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp")
    assert spec.url == "http://127.0.0.1:8000/mcp"


# --- MCPServerWireSpec validation ---


def test_requires_slug_or_url():
    with pytest.raises(ValidationError, match="requires either"):
        MCPServerWireSpec()


def test_rejects_both_slug_and_url():
    with pytest.raises(ValidationError, match="cannot have both"):
        MCPServerWireSpec(slug="dedalus-labs/example-server", url="http://localhost:8000/mcp")


def test_url_must_start_with_http():
    with pytest.raises(ValidationError, match="must start with http://"):
        MCPServerWireSpec(url="localhost:8000/mcp")


def test_https_url_accepted():
    spec = MCPServerWireSpec(url="https://mcp.dedaluslabs.ai/acme/my-server/mcp")
    assert spec.url == "https://mcp.dedaluslabs.ai/acme/my-server/mcp"


def test_localhost_url_accepted():
    spec = MCPServerWireSpec(url="http://127.0.0.1:8000/mcp")
    assert spec.url == "http://127.0.0.1:8000/mcp"


def test_slug_format_validation():
    MCPServerWireSpec(slug="dedalus-labs/example-server")
    MCPServerWireSpec(slug="org_123/project_456")
    MCPServerWireSpec(slug="a/b")

    with pytest.raises(ValidationError):
        MCPServerWireSpec(slug="invalid-no-slash")

    with pytest.raises(ValidationError):
        MCPServerWireSpec(slug="too/many/slashes")


def test_slug_with_at_sign_rejected():
    """Slug pattern doesn't allow @. Use from_slug() for version parsing."""
    with pytest.raises(ValidationError):
        MCPServerWireSpec(slug="org/project@v1", version="v2")

    spec = MCPServerWireSpec.from_slug("org/project@v1")
    assert spec.slug == "org/project"
    assert spec.version == "v1"


def test_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        MCPServerWireSpec(slug="org/test", unknown_field="value")  # type: ignore[call-arg]


# --- MCPServerWireSpec serialization ---


def test_simple_slug_serializes_to_string():
    wire = MCPServerWireSpec.from_slug("dedalus-labs/example-server").to_wire()
    assert wire == "dedalus-labs/example-server"
    assert isinstance(wire, str)


def test_versioned_slug_serializes_to_dict():
    wire = MCPServerWireSpec.from_slug("dedalus-labs/example-server", version="v1.0.0").to_wire()
    assert wire == {"slug": "dedalus-labs/example-server", "version": "v1.0.0"}


def test_url_spec_serializes_to_dict():
    wire = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp").to_wire()
    assert wire == {"url": "http://127.0.0.1:8000/mcp"}


def test_serialization_json_roundtrip():
    wire = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp").to_wire()
    assert '"url": "http://127.0.0.1:8000/mcp"' in json.dumps(wire)


# --- MCPServerProtocol ---


def test_fake_server_satisfies_protocol():
    server = FakeMCPServer(name="test", url="http://localhost:8000/mcp")
    assert is_mcp_server(server)
    assert isinstance(server, MCPServerProtocol)


def test_string_not_protocol():
    assert not is_mcp_server("dedalus-labs/example-server")


def test_dict_not_protocol():
    assert not is_mcp_server({"name": "test", "url": "http://localhost/mcp"})


def test_incomplete_server_not_protocol():
    assert not is_mcp_server(IncompleteServer())


# --- serialize_mcp_servers ---


def test_serialize_none():
    assert serialize_mcp_servers(None) == []


def test_serialize_single_slug():
    assert serialize_mcp_servers("dedalus-labs/example-server") == ["dedalus-labs/example-server"]


def test_serialize_single_url():
    assert serialize_mcp_servers("http://localhost:8000/mcp") == ["http://localhost:8000/mcp"]


def test_serialize_server_object():
    server = FakeMCPServer(name="calculator", url="http://127.0.0.1:8000/mcp")
    assert serialize_mcp_servers(server) == [{"url": "http://127.0.0.1:8000/mcp"}]


def test_serialize_slug_list():
    result = serialize_mcp_servers(["dedalus-labs/example-server", "dedalus-labs/weather"])
    assert result == ["dedalus-labs/example-server", "dedalus-labs/weather"]


def test_serialize_versioned_slug():
    result = serialize_mcp_servers(["dedalus-labs/example-server@v2"])
    assert result == [{"slug": "dedalus-labs/example-server", "version": "v2"}]


def test_serialize_mixed_list():
    server = FakeMCPServer(name="local", url="http://127.0.0.1:8000/mcp")
    result = serialize_mcp_servers([server, "dedalus-labs/example-server", "dedalus-labs/weather@v2"])

    assert len(result) == 3
    assert result[0] == {"url": "http://127.0.0.1:8000/mcp"}
    assert result[1] == "dedalus-labs/example-server"
    assert result[2] == {"slug": "dedalus-labs/weather", "version": "v2"}


def test_serialize_server_without_url():
    server = FakeMCPServer(name="org/my-server", url=None)
    assert serialize_mcp_servers(server) == ["org/my-server"]


def test_serialize_dict_input():
    result = serialize_mcp_servers([{"slug": "dedalus-labs/test"}])
    assert result == ["dedalus-labs/test"]


def test_serialize_dict_url_input():
    """URL dicts must not be rejected by slug validation."""
    result = serialize_mcp_servers([{"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp"}])
    assert result == [{"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp"}]


# --- JSON compatibility ---


def test_full_payload_json_roundtrip():
    server = FakeMCPServer(name="calculator", url="http://127.0.0.1:8000/mcp")
    wire_data = serialize_mcp_servers([server, "dedalus-labs/example-server", "dedalus-labs/weather@v2"])
    payload = {
        "model": "openai/gpt-5-nano",
        "messages": [{"role": "user", "content": "What is 2 + 2?"}],
        "mcp_servers": wire_data,
    }
    parsed = json.loads(json.dumps(payload))
    assert parsed["mcp_servers"][0] == {"url": "http://127.0.0.1:8000/mcp"}
    assert parsed["mcp_servers"][1] == "dedalus-labs/example-server"
    assert parsed["mcp_servers"][2]["slug"] == "dedalus-labs/weather"


def test_unicode_in_url():
    spec = MCPServerWireSpec(url="http://mcp.dedaluslabs.ai/acme/計算機/mcp")
    assert "計算機" in json.dumps(spec.to_wire(), ensure_ascii=False)
