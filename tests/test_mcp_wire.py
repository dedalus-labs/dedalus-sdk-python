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
    MCPServerWireSpec,
    serialize_mcp_servers,
    MCPServerProtocol,
    is_mcp_server,
)


# --- Fixtures ----------------------------------------------------------------


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
    """Missing required protocol attributes (no url, no serve)."""

    def __init__(self) -> None:
        self.name = "incomplete"


# --- MCPServerWireSpec Construction ------------------------------------------


class TestMCPServerWireSpecConstruction:
    """Factory methods for creating wire specs."""

    def test_from_slug_simple(self) -> None:
        """Simple marketplace slug."""
        spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server")
        assert spec.slug == "dedalus-labs/example-server"
        assert spec.version is None

    def test_from_slug_with_version(self) -> None:
        """Slug with explicit version parameter."""
        spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server", version="v1.2.0")
        assert spec.version == "v1.2.0"

    def test_from_slug_with_embedded_version(self) -> None:
        """Slug@version syntax parsed correctly."""
        spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server@v2")
        assert spec.slug == "dedalus-labs/example-server"
        assert spec.version == "v2"

    def test_from_url(self) -> None:
        """Direct URL."""
        spec = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp")
        assert spec.url == "http://127.0.0.1:8000/mcp"


# --- MCPServerWireSpec Validation --------------------------------------------


class TestMCPServerWireSpecValidation:
    """Pydantic validation rules for wire specs."""

    def test_requires_slug_or_url(self) -> None:
        """Must provide either slug or url."""
        with pytest.raises(ValidationError) as exc_info:
            MCPServerWireSpec()
        assert "requires either 'slug' or 'url'" in str(exc_info.value)

    def test_rejects_both_slug_and_url(self) -> None:
        """Cannot provide both slug and url."""
        with pytest.raises(ValidationError) as exc_info:
            MCPServerWireSpec(
                slug="dedalus-labs/example-server",
                url="http://localhost:8000/mcp",
            )
        assert "cannot have both" in str(exc_info.value)

    def test_url_must_start_with_http(self) -> None:
        """URL must have http:// or https:// scheme."""
        with pytest.raises(ValidationError) as exc_info:
            MCPServerWireSpec(url="localhost:8000/mcp")
        assert "must start with http://" in str(exc_info.value)

    def test_https_url_accepted(self) -> None:
        """HTTPS URLs are valid."""
        spec = MCPServerWireSpec(url="https://mcp.dedaluslabs.ai/acme/my-server/mcp")
        assert spec.url == "https://mcp.dedaluslabs.ai/acme/my-server/mcp"

    def test_localhost_url_accepted(self) -> None:
        """Localhost URLs are valid for dev."""
        spec = MCPServerWireSpec(url="http://127.0.0.1:8000/mcp")
        assert spec.url == "http://127.0.0.1:8000/mcp"

    def test_slug_format_validation(self) -> None:
        """Slug must match org/project pattern."""
        MCPServerWireSpec(slug="dedalus-labs/example-server")
        MCPServerWireSpec(slug="org_123/project_456")
        MCPServerWireSpec(slug="a/b")

        with pytest.raises(ValidationError):
            MCPServerWireSpec(slug="invalid-no-slash")

        with pytest.raises(ValidationError):
            MCPServerWireSpec(slug="too/many/slashes")

    def test_slug_with_at_sign_rejected_by_pattern(self) -> None:
        """Slug pattern doesn't allow @ - use from_slug() for version parsing."""
        with pytest.raises(ValidationError) as exc_info:
            MCPServerWireSpec(slug="org/project@v1", version="v2")
        assert "string_pattern_mismatch" in str(exc_info.value).lower()

        # Correct way: use from_slug() which parses the version
        spec = MCPServerWireSpec.from_slug("org/project@v1")
        assert spec.slug == "org/project"
        assert spec.version == "v1"

    def test_extra_fields_forbidden(self) -> None:
        """Extra fields rejected (ConfigDict extra='forbid')."""
        with pytest.raises(ValidationError) as exc_info:
            MCPServerWireSpec(slug="org/test", unknown_field="value")  # type: ignore[call-arg]
        assert "extra" in str(exc_info.value).lower()


# --- MCPServerWireSpec Serialization -----------------------------------------


class TestMCPServerWireSpecSerialization:
    """to_wire() output for different spec types."""

    def test_simple_slug_serializes_to_string(self) -> None:
        """Simple slug-only specs serialize to plain string (efficient)."""
        spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server")
        wire = spec.to_wire()
        assert wire == "dedalus-labs/example-server"
        assert isinstance(wire, str)

    def test_versioned_slug_serializes_to_dict(self) -> None:
        """Slug with version serializes to dict."""
        spec = MCPServerWireSpec.from_slug("dedalus-labs/example-server", version="v1.0.0")
        wire = spec.to_wire()
        assert wire == {"slug": "dedalus-labs/example-server", "version": "v1.0.0"}

    def test_url_spec_serializes_to_dict(self) -> None:
        """URL-based specs serialize to dict with just url."""
        spec = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp")
        wire = spec.to_wire()
        assert wire == {"url": "http://127.0.0.1:8000/mcp"}

    def test_serialization_is_json_compatible(self) -> None:
        """Wire format round-trips through JSON."""
        spec = MCPServerWireSpec.from_url(url="http://127.0.0.1:8000/mcp")
        json_str = json.dumps(spec.to_wire())
        assert '"url": "http://127.0.0.1:8000/mcp"' in json_str


# --- MCPServerProtocol -------------------------------------------------------


class TestMCPServerProtocol:
    """Structural typing for MCP server objects."""

    def test_fake_server_satisfies_protocol(self) -> None:
        """FakeMCPServer satisfies MCPServerProtocol."""
        server = FakeMCPServer(name="test", url="http://localhost:8000/mcp")
        assert is_mcp_server(server)
        assert isinstance(server, MCPServerProtocol)

    def test_string_does_not_satisfy_protocol(self) -> None:
        """Plain strings are not MCPServerProtocol."""
        assert not is_mcp_server("dedalus-labs/example-server")

    def test_dict_does_not_satisfy_protocol(self) -> None:
        """Dicts are not MCPServerProtocol."""
        assert not is_mcp_server({"name": "test", "url": "http://localhost/mcp"})

    def test_incomplete_server_does_not_satisfy(self) -> None:
        """Missing attributes means protocol not satisfied."""
        assert not is_mcp_server(IncompleteServer())


# --- serialize_mcp_servers ---------------------------------------------------


class TestSerializeMCPServers:
    """End-to-end serialization of mixed mcp_servers input."""

    def test_none_returns_empty_list(self) -> None:
        """None input returns empty list."""
        assert serialize_mcp_servers(None) == []

    def test_single_string_slug(self) -> None:
        """Single slug string passes through."""
        assert serialize_mcp_servers("dedalus-labs/example-server") == ["dedalus-labs/example-server"]

    def test_single_string_url(self) -> None:
        """Single URL string passes through."""
        assert serialize_mcp_servers("http://localhost:8000/mcp") == ["http://localhost:8000/mcp"]

    def test_single_mcp_server_object(self) -> None:
        """MCPServerProtocol object serializes to URL dict."""
        server = FakeMCPServer(name="calculator", url="http://127.0.0.1:8000/mcp")
        result = serialize_mcp_servers(server)
        assert result == [{"url": "http://127.0.0.1:8000/mcp"}]

    def test_list_of_slugs(self) -> None:
        """List of slug strings."""
        result = serialize_mcp_servers(["dedalus-labs/example-server", "dedalus-labs/weather"])
        assert result == ["dedalus-labs/example-server", "dedalus-labs/weather"]

    def test_versioned_slug_in_list(self) -> None:
        """Slug@version syntax expands to dict."""
        result = serialize_mcp_servers(["dedalus-labs/example-server@v2"])
        assert result == [{"slug": "dedalus-labs/example-server", "version": "v2"}]

    def test_mixed_list(self) -> None:
        """Mixed list of slugs, URLs, and server objects."""
        server = FakeMCPServer(name="local", url="http://127.0.0.1:8000/mcp")
        result = serialize_mcp_servers([server, "dedalus-labs/example-server", "dedalus-labs/weather@v2"])

        assert len(result) == 3
        assert result[0] == {"url": "http://127.0.0.1:8000/mcp"}
        assert result[1] == "dedalus-labs/example-server"
        assert result[2] == {"slug": "dedalus-labs/weather", "version": "v2"}

    def test_server_without_url_uses_name_as_slug(self) -> None:
        """Server object without URL returns name as slug."""
        server = FakeMCPServer(name="org/my-server", url=None)
        result = serialize_mcp_servers(server)
        assert result == ["org/my-server"]

    def test_dict_input_validated(self) -> None:
        """Dict inputs pass through MCPServerWireSpec validation."""
        result = serialize_mcp_servers([{"slug": "dedalus-labs/test"}])
        assert result == ["dedalus-labs/test"]


# --- JSON Compatibility ------------------------------------------------------


class TestJSONCompatibility:
    """Wire format is JSON-serializable and API-compatible."""

    def test_full_payload_structure(self) -> None:
        """Complete API payload round-trips through JSON."""
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

    def test_unicode_in_url(self) -> None:
        """Unicode in URL paths are handled."""
        # Dedalus-hosted URL with unicode in path token
        spec = MCPServerWireSpec(url="http://mcp.dedaluslabs.ai/acme/計算機/mcp")
        result = spec.to_wire()
        json_str = json.dumps(result, ensure_ascii=False)
        assert "計算機" in json_str
