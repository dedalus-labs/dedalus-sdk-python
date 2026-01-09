# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for Connection/Credential wire format serialization."""

from __future__ import annotations

from typing import Any

import pytest

from dedalus_labs.lib.mcp import (
    serialize_connection,
    collect_unique_connections,
    match_credentials_to_connections,
    validate_credentials_for_servers,
)


# --- Mock objects for testing ---


class MockConnection:
    """Mock Connection object implementing the protocol."""

    def __init__(
        self,
        name: str,
        base_url: str | None = None,
        timeout_ms: int = 30000,
    ) -> None:
        self._name = name
        self._base_url = base_url
        self._timeout_ms = timeout_ms

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_url(self) -> str | None:
        return self._base_url

    @property
    def timeout_ms(self) -> int:
        return self._timeout_ms

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"name": self._name}
        if self._base_url is not None:
            result["base_url"] = self._base_url
        if self._timeout_ms != 30000:
            result["timeout_ms"] = self._timeout_ms
        return result


class MockCredential:
    """Mock Secret object implementing the protocol."""

    def __init__(self, connection: MockConnection, **values: Any) -> None:
        self._connection = connection
        self._values = values

    @property
    def connection(self) -> MockConnection:
        return self._connection

    @property
    def values(self) -> dict[str, Any]:
        return dict(self._values)

    def to_dict(self) -> dict[str, Any]:
        return {
            "connection_name": self._connection.name,
            "values": dict(self._values),
        }

    def values_for_encryption(self) -> dict[str, Any]:
        return dict(self._values)


class TestSerializeConnection:
    """Test serialize_connection helper."""

    def test_with_connection_object(self) -> None:
        """Serialize Connection object with to_dict()."""
        conn = MockConnection("github", "https://api.github.com", 60000)

        result = serialize_connection(conn)

        assert result["name"] == "github"
        assert result["base_url"] == "https://api.github.com"
        assert result["timeout_ms"] == 60000

    def test_with_dict(self) -> None:
        """Pass-through for dict input."""
        data = {"name": "dedalus", "base_url": "https://api.dedaluslabs.ai/v1"}

        result = serialize_connection(data)

        assert result == data

    def test_duck_type_extraction(self) -> None:
        """Extract fields from object without to_dict()."""

        class BareConnection:
            name = "bare"
            base_url = "https://bare.api.com"
            timeout_ms = 15000

        result = serialize_connection(BareConnection())

        assert result["name"] == "bare"
        assert result["base_url"] == "https://bare.api.com"
        assert result["timeout_ms"] == 15000


class TestMatchSecretsToConnections:
    """Test match_credentials_to_connections helper."""

    def test_basic_matching(self) -> None:
        """Match secrets to connections by name."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")

        github_secret = MockCredential(github, token="ghp_xxx")
        dedalus_secret = MockCredential(dedalus, api_key="sk_xxx")

        pairs = match_credentials_to_connections(
            [github, dedalus],
            [dedalus_secret, github_secret],  # Different order
        )

        assert len(pairs) == 2
        # Pairs should be in connection order
        assert pairs[0][0].name == "github"
        assert pairs[0][1].values == {"token": "ghp_xxx"}
        assert pairs[1][0].name == "dedalus"
        assert pairs[1][1].values == {"api_key": "sk_xxx"}

    def test_missing_secret_raises(self) -> None:
        """Raise ValueError if connection has no secret."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")

        github_secret = MockCredential(github, token="ghp_xxx")

        with pytest.raises(
            ValueError, match="Missing credentials for connections.*dedalus"
        ):
            match_credentials_to_connections([github, dedalus], [github_secret])

    def test_with_dict_inputs(self) -> None:
        """Works with dict inputs too."""
        connections = [{"name": "api"}]
        secrets = [{"connection_name": "api", "values": {"key": "xxx"}}]

        pairs = match_credentials_to_connections(connections, secrets)

        assert len(pairs) == 1
        assert pairs[0][0]["name"] == "api"
        assert pairs[0][1]["values"] == {"key": "xxx"}

    def test_missing_multiple_secrets(self) -> None:
        """Error message lists all missing secrets."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")
        slack = MockConnection("slack")

        github_secret = MockCredential(github, token="ghp_xxx")

        with pytest.raises(ValueError) as exc:
            match_credentials_to_connections([github, dedalus, slack], [github_secret])

        assert "dedalus" in str(exc.value)
        assert "slack" in str(exc.value)


# --- Mock server for multi-server tests ---


class MockServer:
    """Mock MCPServer for testing."""

    def __init__(self, name: str, connections: list[Any] | None = None) -> None:
        self.name = name
        self.connections = connections or []


class TestCollectUniqueConnections:
    """Test collect_unique_connections helper."""

    def test_single_server(self) -> None:
        """Collect connections from single server."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")
        server = MockServer("bot", connections=[github, dedalus])

        result = collect_unique_connections([server])

        assert len(result) == 2
        assert result[0].name == "github"
        assert result[1].name == "dedalus"

    def test_shared_connection_deduplicated(self) -> None:
        """Shared Connection appears only once."""
        github = MockConnection("github")

        server_a = MockServer("issues", connections=[github])
        server_b = MockServer("prs", connections=[github])

        result = collect_unique_connections([server_a, server_b])

        assert len(result) == 1
        assert result[0].name == "github"

    def test_same_name_different_objects(self) -> None:
        """Connections with same name are deduplicated."""
        # Even if different objects, same name means same logical connection
        github_a = MockConnection("github", base_url="https://api.github.com")
        github_b = MockConnection("github", base_url="https://api.github.com")

        server_a = MockServer("a", connections=[github_a])
        server_b = MockServer("b", connections=[github_b])

        result = collect_unique_connections([server_a, server_b])

        # Should only include first occurrence
        assert len(result) == 1
        assert result[0] is github_a

    def test_multiple_servers_multiple_connections(self) -> None:
        """Collect and deduplicate across multiple servers."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")
        slack = MockConnection("slack")

        server_a = MockServer("bot1", connections=[github, dedalus])
        server_b = MockServer("bot2", connections=[github, slack])

        result = collect_unique_connections([server_a, server_b])

        assert len(result) == 3
        names = [c.name for c in result]
        assert names == ["github", "dedalus", "slack"]

    def test_server_without_connections(self) -> None:
        """Handle servers with no connections."""
        server_a = MockServer("empty")
        server_b = MockServer("has", connections=[MockConnection("api")])

        result = collect_unique_connections([server_a, server_b])

        assert len(result) == 1


class TestValidateSecretsForServers:
    """Test validate_credentials_for_servers (main SDK init validation)."""

    def test_all_connections_have_secrets(self) -> None:
        """Success when all connections have matching secrets."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")

        server = MockServer("bot", connections=[github, dedalus])

        github_secret = MockCredential(github, token="ghp_xxx")
        dedalus_secret = MockCredential(dedalus, api_key="sk_xxx")

        pairs = validate_credentials_for_servers(
            [server], [github_secret, dedalus_secret]
        )

        assert len(pairs) == 2

    def test_shared_connection_one_secret(self) -> None:
        """One Secret covers shared Connection across servers."""
        github = MockConnection("github")

        server_a = MockServer("issues", connections=[github])
        server_b = MockServer("prs", connections=[github])

        github_secret = MockCredential(github, token="ghp_xxx")

        pairs = validate_credentials_for_servers(
            [server_a, server_b],
            [github_secret],  # Only one secret needed
        )

        assert len(pairs) == 1
        assert pairs[0][0].name == "github"

    def test_missing_secret_fails_fast(self) -> None:
        """Raise immediately if any connection lacks a secret."""
        github = MockConnection("github")
        dedalus = MockConnection("dedalus")

        server = MockServer("bot", connections=[github, dedalus])
        github_secret = MockCredential(github, token="ghp_xxx")

        with pytest.raises(ValueError) as exc:
            validate_credentials_for_servers([server], [github_secret])

        assert "dedalus" in str(exc.value)
        assert "Missing credentials" in str(exc.value)
