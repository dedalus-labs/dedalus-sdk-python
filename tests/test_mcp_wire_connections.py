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


# --- Test helpers ---


class MockConnection:
    def __init__(self, name: str, base_url: str | None = None, timeout_ms: int = 30000) -> None:
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
        return {"connection_name": self._connection.name, "values": dict(self._values)}

    def values_for_encryption(self) -> dict[str, Any]:
        return dict(self._values)


class MockServer:
    def __init__(self, name: str, connections: list[Any] | None = None) -> None:
        self.name = name
        self.connections = connections or []


# --- serialize_connection ---


def test_serialize_connection_object():
    conn = MockConnection("github", "https://api.github.com", 60000)
    result = serialize_connection(conn)
    assert result["name"] == "github"
    assert result["base_url"] == "https://api.github.com"
    assert result["timeout_ms"] == 60000


def test_serialize_connection_dict():
    data = {"name": "dedalus", "base_url": "https://api.dedaluslabs.ai/v1"}
    assert serialize_connection(data) == data


def test_serialize_connection_duck_type():
    class BareConnection:
        name = "bare"
        base_url = "https://bare.api.com"
        timeout_ms = 15000

    result = serialize_connection(BareConnection())
    assert result["name"] == "bare"
    assert result["base_url"] == "https://bare.api.com"
    assert result["timeout_ms"] == 15000


# --- match_credentials_to_connections ---


def test_match_basic():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    pairs = match_credentials_to_connections(
        [github, dedalus],
        [MockCredential(dedalus, api_key="sk_xxx"), MockCredential(github, token="ghp_xxx")],
    )
    assert len(pairs) == 2
    assert pairs[0][0].name == "github"
    assert pairs[0][1].values == {"token": "ghp_xxx"}
    assert pairs[1][0].name == "dedalus"
    assert pairs[1][1].values == {"api_key": "sk_xxx"}


def test_match_missing_raises():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    with pytest.raises(ValueError, match="Missing credentials for connections.*dedalus"):
        match_credentials_to_connections([github, dedalus], [MockCredential(github, token="ghp_xxx")])


def test_match_with_dicts():
    connections = [{"name": "api"}]
    secrets = [{"connection_name": "api", "values": {"key": "xxx"}}]
    pairs = match_credentials_to_connections(connections, secrets)
    assert len(pairs) == 1
    assert pairs[0][0]["name"] == "api"
    assert pairs[0][1]["values"] == {"key": "xxx"}


def test_match_missing_multiple():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    slack = MockConnection("slack")
    with pytest.raises(ValueError) as exc:
        match_credentials_to_connections([github, dedalus, slack], [MockCredential(github, token="ghp_xxx")])
    assert "dedalus" in str(exc.value)
    assert "slack" in str(exc.value)


# --- collect_unique_connections ---


def test_collect_single_server():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    result = collect_unique_connections([MockServer("bot", connections=[github, dedalus])])
    assert len(result) == 2
    assert result[0].name == "github"
    assert result[1].name == "dedalus"


def test_collect_deduplicates_shared():
    github = MockConnection("github")
    result = collect_unique_connections([MockServer("a", [github]), MockServer("b", [github])])
    assert len(result) == 1
    assert result[0].name == "github"


def test_collect_deduplicates_by_name():
    github_a = MockConnection("github", base_url="https://api.github.com")
    github_b = MockConnection("github", base_url="https://api.github.com")
    result = collect_unique_connections([MockServer("a", [github_a]), MockServer("b", [github_b])])
    assert len(result) == 1
    assert result[0] is github_a


def test_collect_multiple_servers():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    slack = MockConnection("slack")
    result = collect_unique_connections([
        MockServer("bot1", [github, dedalus]),
        MockServer("bot2", [github, slack]),
    ])
    assert [c.name for c in result] == ["github", "dedalus", "slack"]


def test_collect_server_without_connections():
    result = collect_unique_connections([MockServer("empty"), MockServer("has", [MockConnection("api")])])
    assert len(result) == 1


# --- validate_credentials_for_servers ---


def test_validate_all_present():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    server = MockServer("bot", connections=[github, dedalus])
    pairs = validate_credentials_for_servers(
        [server],
        [MockCredential(github, token="ghp_xxx"), MockCredential(dedalus, api_key="sk_xxx")],
    )
    assert len(pairs) == 2


def test_validate_shared_connection():
    github = MockConnection("github")
    pairs = validate_credentials_for_servers(
        [MockServer("a", [github]), MockServer("b", [github])],
        [MockCredential(github, token="ghp_xxx")],
    )
    assert len(pairs) == 1
    assert pairs[0][0].name == "github"


def test_validate_missing_fails_fast():
    github = MockConnection("github")
    dedalus = MockConnection("dedalus")
    server = MockServer("bot", connections=[github, dedalus])
    with pytest.raises(ValueError) as exc:
        validate_credentials_for_servers([server], [MockCredential(github, token="ghp_xxx")])
    assert "dedalus" in str(exc.value)
    assert "Missing credentials" in str(exc.value)
