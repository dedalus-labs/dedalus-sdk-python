# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP server wire format serialization.

Converts MCPServer objects and various input formats to the API wire format.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing_extensions import TypeAlias

from .protocols import MCPServerProtocol, CredentialProtocol, is_mcp_server

__all__ = [
    # Core types
    "MCPServerWireSpec",
    # Serialization
    "serialize_mcp_servers",
    "serialize_credentials",
    "serialize_connection",
    "serialize_mcp_server_with_creds",
    "serialize_tool_specs",
    # Credential matching
    "match_credentials_to_server",
    "match_credentials_to_connections",
    "validate_credentials_for_servers",
    # Helpers
    "build_connection_record",
    "collect_unique_connections",
]


# ---------------------------------------------------------------------------
# Type Aliases
# ---------------------------------------------------------------------------

# Serialized wire output: slug string or spec dict
MCPServerWireOutput: TypeAlias = Union[str, Dict[str, Any]]

# Input types that serialize_mcp_servers accepts
MCPServerInput: TypeAlias = Union[str, Dict[str, Any], MCPServerProtocol]

# Connection/credential pair for provisioning
ConnectionCredentialPair: TypeAlias = Tuple[Any, CredentialProtocol]


# ---------------------------------------------------------------------------
# Wire Format Model (for validation during serialization)
# ---------------------------------------------------------------------------


class MCPServerWireSpec(BaseModel):
    """MCP server spec for API transmission.

    Wire format: either slug or url (not both).
    """

    model_config = ConfigDict(extra="forbid")

    slug: Optional[str] = Field(
        default=None,
        pattern=r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$",
        description="Marketplace identifier (org/name format)",
    )
    url: Optional[str] = Field(
        default=None,
        description="MCP server URL endpoint",
    )
    version: Optional[str] = Field(
        default=None,
        description="Version for MCP servers",
    )

    @model_validator(mode="after")
    def validate_slug_or_url(self) -> MCPServerWireSpec:
        """Require exactly one of slug or url."""
        has_slug = self.slug is not None
        has_url = self.url is not None

        if not has_slug and not has_url:
            raise ValueError("requires either 'slug' or 'url'")
        if has_slug and has_url:
            raise ValueError("cannot have both 'slug' and 'url'")
        if has_slug and self.version and self.slug and "@" in self.slug:
            raise ValueError("cannot specify both 'version' field and version in slug")

        return self

    @field_validator("url")
    @classmethod
    def validate_url_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate URL scheme."""
        if v is None:
            return None
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"URL must start with http:// or https://, got: {v}")
        return v

    def to_wire(self) -> MCPServerWireOutput:
        """Convert to wire format. Simple slugs become strings."""
        if self.slug and not self.version:
            return self.slug
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_slug(cls, slug: str, version: Optional[str] = None) -> MCPServerWireSpec:
        """Create from slug, extracting version if embedded."""
        if "@" in slug and version is None:
            slug, version = slug.rsplit("@", 1)
        return cls(slug=slug, version=version)

    @classmethod
    def from_url(cls, url: str) -> MCPServerWireSpec:
        """Create from direct URL."""
        return cls(url=url)


# ---------------------------------------------------------------------------
# MCP Server Serialization
# ---------------------------------------------------------------------------


def serialize_mcp_servers(
    servers: Union[MCPServerInput, Sequence[MCPServerInput], None],
) -> List[MCPServerWireOutput]:
    """Convert mcp_servers input to API wire format.

    Accepts:
        - Single slug string ("org/server" or "org/server@v1")
        - Single URL string ("https://...")
        - Single MCPServer object (from dedalus_mcp)
        - Single dict matching MCPServerSpec
        - Sequence of any of the above
        - None (returns empty list)

    Returns:
        List of wire format items (strings or dicts).

    """
    if servers is None:
        return []
    if isinstance(servers, str):
        return [_serialize_single(servers)]
    if isinstance(servers, dict):
        return [_serialize_single(cast(Dict[str, Any], servers))]
    if is_mcp_server(servers):
        return [_serialize_single(cast(MCPServerProtocol, servers))]

    # Sequence of inputs
    return [_serialize_single(item) for item in servers]


def _serialize_single(item: MCPServerInput) -> MCPServerWireOutput:
    """Serialize a single MCP server input to wire format."""
    if isinstance(item, str):
        # URL passthrough
        if item.startswith(("http://", "https://")):
            return item
        # Slug with embedded version
        if "@" in item:
            slug, version = item.rsplit("@", 1)
            return MCPServerWireSpec.from_slug(slug, version).to_wire()
        # Simple slug
        return item

    if is_mcp_server(item):
        # MCPServer object - check for URL first
        url = getattr(item, "url", None)
        if url is not None:
            return MCPServerWireSpec.from_url(url).to_wire()

        # Fall back to name (slug)
        name = getattr(item, "name", None)
        if name is not None:
            return name

        raise ValueError("MCP server must have either 'url' or 'name' attribute")

    if isinstance(item, dict):
        # Validate and convert dict
        return MCPServerWireSpec.model_validate(item).to_wire()

    # Fallback for unknown types
    return str(item)


# ---------------------------------------------------------------------------
# Credential Serialization
# ---------------------------------------------------------------------------


def serialize_credentials(creds: Optional[CredentialProtocol]) -> Optional[Dict[str, Any]]:
    """Serialize Credentials schema to wire format.

    Args:
        creds: Credentials object with to_dict() method, or None.

    Returns:
        Dict mapping field names to binding specs, or None.
    """
    if creds is None:
        return None
    if hasattr(creds, "to_dict"):
        return creds.to_dict()
    return None


def serialize_tool_specs(tools_service: Any) -> Dict[str, Dict[str, Any]]:
    """Serialize tool specs to intents manifest format.

    Args:
        tools_service: Tools service from MCPServer with _tool_specs attribute.

    Returns:
        Dict mapping tool names to {description, schema} dicts.
    """
    specs = getattr(tools_service, "_tool_specs", {})
    if not specs:
        return {}

    manifest: Dict[str, Dict[str, Any]] = {}
    for name, spec in specs.items():
        if hasattr(spec, "description"):
            manifest[name] = {
                "description": spec.description,
                "schema": getattr(spec, "input_schema", {}),
            }
        elif isinstance(spec, dict):
            manifest[name] = {
                "description": spec.get("description", ""),
                "schema": spec.get("input_schema", {}),
            }
    return manifest


def serialize_mcp_server_with_creds(server: MCPServerProtocol) -> Dict[str, Any]:
    """Serialize MCPServer with credentials for connection provisioning.

    Args:
        server: MCPServer object with credentials/connection attributes.

    Returns:
        Dict with server config (credential values added separately).
    """
    result: Dict[str, Any] = {"name": getattr(server, "name", "unknown")}

    creds = getattr(server, "credentials", None)
    if creds is not None:
        creds_dict = serialize_credentials(creds)
        if creds_dict:
            result["credentials"] = creds_dict

    connection = getattr(server, "connection", None)
    if connection:
        result["connection"] = connection

    return result


# ---------------------------------------------------------------------------
# Connection Serialization
# ---------------------------------------------------------------------------


def serialize_connection(connection: Any) -> Dict[str, Any]:
    """Serialize a Connection object to wire format.

    Works with any Connection-like object that provides:
        - to_dict() method, OR
        - name, base_url, timeout_ms attributes

    Args:
        connection: Connection object or dict.

    Returns:
        Dict with name, base_url, timeout_ms fields.
    """
    if hasattr(connection, "to_dict"):
        return connection.to_dict()
    if isinstance(connection, dict):
        return connection
    # Duck-type extraction
    return {
        "name": getattr(connection, "name", "unknown"),
        "base_url": getattr(connection, "base_url", None),
        "timeout_ms": getattr(connection, "timeout_ms", 30000),
    }


def collect_unique_connections(servers: Sequence[MCPServerProtocol]) -> List[Any]:
    """Collect unique connections from multiple MCPServer instances.

    Args:
        servers: List of MCPServer objects.

    Returns:
        List of unique Connection objects.
    """
    seen_names: set[str] = set()
    unique: List[Any] = []

    for server in servers:
        connections = getattr(server, "connections", {})
        # Handle both dict and list formats
        conn_list = list(connections.values()) if isinstance(connections, dict) else list(connections or [])

        for conn in conn_list:
            name = (
                getattr(conn, "name", None)
                if hasattr(conn, "name")
                else conn.get("name")
                if isinstance(conn, dict)
                else None
            )
            if name and name not in seen_names:
                seen_names.add(name)
                unique.append(conn)

    return unique


# ---------------------------------------------------------------------------
# Credential Matching
# ---------------------------------------------------------------------------


def match_credentials_to_server(
    server: MCPServerProtocol,
    credentials: Dict[str, Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Match credentials dict to server.connection.

    Args:
        server: MCPServer with optional connection field.
        credentials: Dict mapping connection names to credential dicts.

    Returns:
        Matched credential values, or None if no connection.

    Raises:
        KeyError: If server.connection not found in credentials.

    """
    connection = getattr(server, "connection", None)
    if not connection:
        return None
    if connection not in credentials:
        raise KeyError(f"No credentials found for connection '{connection}'")
    return credentials[connection]


def match_credentials_to_connections(
    connections: Sequence[Any],
    credentials: Sequence[CredentialProtocol],
) -> List[ConnectionCredentialPair]:
    """Match Credential objects to their Connection definitions.

    Args:
        connections: List of Connection objects.
        credentials: List of Credential objects.

    Returns:
        List of (connection, credential) pairs.

    Raises:
        ValueError: If any connection lacks a matching credential.
    """
    # Build lookup by connection name
    creds_by_name: Dict[str, CredentialProtocol] = {}
    for cred in credentials:
        if hasattr(cred, "connection"):
            name = getattr(cred.connection, "name", None)
        elif isinstance(cred, dict):
            name = cred.get("connection_name")
        else:
            continue
        if name:
            creds_by_name[name] = cred

    # Match connections to credentials
    pairs: List[ConnectionCredentialPair] = []
    missing: List[str] = []

    for conn in connections:
        name = (
            getattr(conn, "name", None)
            if hasattr(conn, "name")
            else conn.get("name")
            if isinstance(conn, dict)
            else None
        )
        if name and name in creds_by_name:
            pairs.append((conn, creds_by_name[name]))
        elif name:
            missing.append(name)

    if missing:
        raise ValueError(
            f"Missing credentials for connections: {sorted(missing)}. "
            f"Each Connection declared in mcp_servers must have a corresponding Credential."
        )

    return pairs


def validate_credentials_for_servers(
    servers: Sequence[MCPServerProtocol],
    credentials: Sequence[CredentialProtocol],
) -> List[ConnectionCredentialPair]:
    """Validate that all connections across servers have credentials.

    Main entry point for SDK initialization validation. Collects unique
    connections from all servers and ensures each has a matching Credential.

    Args:
        servers: List of MCPServer objects.
        credentials: List of Credential objects.

    Returns:
        List of (connection, credential) pairs ready for provisioning.

    Raises:
        ValueError: If any connection lacks a credential (fail-fast at init).
    """
    connections = collect_unique_connections(servers)
    return match_credentials_to_connections(connections, credentials)


def build_connection_record(
    server: MCPServerProtocol,
    credentials: Dict[str, Dict[str, Any]],
    org_id: str,
) -> Dict[str, Any]:
    """Build a connection record.

    Args:
        server: MCPServer object.
        credentials: Dict mapping connection names to credential values.
        org_id: Organization ID for the connection.

    Returns:
        Connection record payload.

    """
    matched_creds = match_credentials_to_server(server, credentials)

    return {
        "org_id": org_id,
        "connection": getattr(server, "connection", None),
        "credentials": serialize_credentials(getattr(server, "credentials", None)),
        "credential_values": matched_creds,
    }
