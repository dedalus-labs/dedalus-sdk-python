# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP server wire format"""

from __future__ import annotations

from typing import Any, Dict, List, Union, Optional, Sequence

from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

# --- Pydantic Models ---------------------------------------------------------


class MCPServerWireSpec(BaseModel):
    """MCP server spec for API transmission. Either slug or url, not both."""

    model_config = ConfigDict(extra='forbid')

    slug: Optional[str] = Field(
        default=None, pattern=r'^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    )
    version: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    @model_validator(mode='after')
    def validate_slug_or_url(self) -> 'MCPServerWireSpec':
        has_slug = self.slug is not None
        has_url = self.url is not None

        if not has_slug and not has_url:
            raise ValueError("requires either 'slug' or 'url'")
        if has_slug and has_url:
            raise ValueError("cannot have both 'slug' and 'url'")
        if has_slug and self.version and '@' in self.slug:
            raise ValueError("cannot specify both 'version' field and version in slug")

        return self

    @field_validator('url')
    @classmethod
    def validate_url_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v.startswith(('http://', 'https://')):
            raise ValueError(f'URL must start with http:// or https://, got: {v}')
        return v

    def to_wire(self) -> Union[str, Dict[str, Any]]:
        """Simple slugs become strings, everything else becomes a dict."""
        if self.slug and not self.version:
            return self.slug
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_slug(cls, slug: str, version: Optional[str] = None) -> 'MCPServerWireSpec':
        if '@' in slug and version is None:
            slug, version = slug.rsplit('@', 1)
        return cls(slug=slug, version=version)

    @classmethod
    def from_url(cls, url: str) -> 'MCPServerWireSpec':
        return cls(url=url)


# --- Serialization -----------------------------------------------------------


def serialize_mcp_servers(
    servers: Union[str, Sequence[Union[str, Any]], Any, None],
) -> List[Union[str, Dict[str, Any]]]:
    """Convert mcp_servers to API wire format. Handles strings, objects, or sequences."""
    from .protocols import is_mcp_server

    if servers is None:
        return []
    if isinstance(servers, str):
        return [_serialize_single(servers)]
    if is_mcp_server(servers):
        return [_serialize_single(servers)]
    return [_serialize_single(item) for item in servers]


def _serialize_single(item: Union[str, Any]) -> Union[str, Dict[str, Any]]:
    from .protocols import is_mcp_server

    if isinstance(item, str):
        if item.startswith(('http://', 'https://')):
            return item
        if '@' in item:
            slug, version = item.rsplit('@', 1)
            return MCPServerWireSpec.from_slug(slug, version).to_wire()
        return item

    if is_mcp_server(item):
        url = getattr(item, 'url', None)
        if url is None:
            name = getattr(item, 'name', 'unknown')
            raise ValueError(
                f"MCP server '{name}' has no URL. Call serve() first or use a slug instead."
            )
        return MCPServerWireSpec.from_url(url).to_wire()

    if isinstance(item, dict):
        return MCPServerWireSpec.model_validate(item).to_wire()

    return str(item)


# --- Credential Serialization ------------------------------------------------


def serialize_credentials(creds: Any) -> Optional[Dict[str, Any]]:
    """Serialize Credentials schema to wire format.

    Args:
        creds: Credentials object with to_dict() method, or None

    Returns:
        Dict mapping field names to binding specs, or None

    """
    if creds is None:
        return None
    if hasattr(creds, 'to_dict'):
        return creds.to_dict()
    return None


def serialize_tool_specs(tools_service: Any) -> Dict[str, Any]:
    """Serialize tool specs to intents manifest format.

    Args:
        tools_service: Tools service from MCPServer with _tool_specs

    Returns:
        Dict mapping tool names to their schemas

    """
    specs = getattr(tools_service, '_tool_specs', {})
    if not specs:
        return {}

    manifest: Dict[str, Any] = {}
    for name, spec in specs.items():
        if hasattr(spec, 'description'):
            manifest[name] = {
                'description': spec.description,
                'schema': getattr(spec, 'input_schema', {}),
            }
        elif isinstance(spec, dict):
            manifest[name] = {
                'description': spec.get('description', ''),
                'schema': spec.get('input_schema', {}),
            }
    return manifest


def serialize_mcp_server_with_creds(server: Any) -> Dict[str, Any]:
    """Serialize MCPServer with credentials for connection provisioning.

    Args:
        server: MCPServer object with credentials/connection

    Returns:
        Dict with server config for API (credential values added separately)

    """
    result: Dict[str, Any] = {'name': getattr(server, 'name', 'unknown')}

    creds = getattr(server, 'credentials', None)
    if creds is not None:
        creds_dict = serialize_credentials(creds)
        if creds_dict:
            result['credentials'] = creds_dict

    connection = getattr(server, 'connection', None)
    if connection:
        result['connection'] = connection

    return result


def match_credentials_to_server(
    server: Any,
    credentials: Dict[str, Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Match credentials dict to server.connection.

    Args:
        server: MCPServer with optional connection field
        credentials: Dict mapping connection names to credential dicts

    Returns:
        Matched credential values, or None if no connection

    Raises:
        KeyError: If server.connection not found in credentials

    """
    connection = getattr(server, 'connection', None)
    if not connection:
        return None
    if connection not in credentials:
        raise KeyError(f"No credentials found for connection '{connection}'")
    return credentials[connection]


def build_connection_record(
    server: Any,
    credentials: Dict[str, Dict[str, Any]],
    org_id: str,
) -> Dict[str, Any]:
    """Build complete connection record for provisioning.

    Args:
        server: MCPServer object
        credentials: Dict mapping connection names to credential values
        org_id: Organization ID for the connection

    Returns:
        Complete connection record for DB storage

    """
    matched_creds = match_credentials_to_server(server, credentials)

    return {
        'org_id': org_id,
        'connection': getattr(server, 'connection', None),
        'credentials': serialize_credentials(getattr(server, 'credentials', None)),
        'credential_values': matched_creds,
    }


def serialize_connection(connection: Any) -> Dict[str, Any]:
    """Serialize a Connection object to wire format.

    Works with any Connection-like object that provides:
    - to_dict() method, OR
    - name, base_url, timeout_ms attributes

    Args:
        connection: Connection object or dict

    Returns:
        Dict with name, base_url, timeout_ms fields

    """
    if hasattr(connection, 'to_dict'):
        return connection.to_dict()
    if isinstance(connection, dict):
        return connection
    # Duck-type extraction for protocol compatibility
    return {
        'name': getattr(connection, 'name', 'unknown'),
        'base_url': getattr(connection, 'base_url', None),
        'timeout_ms': getattr(connection, 'timeout_ms', 30000),
    }


def serialize_credential(credential: Any) -> Dict[str, Any]:
    """Serialize a Credential object to wire format.

    Works with any Credential-like object that provides:
    - to_dict() method, OR
    - connection and values attributes

    Args:
        credential: Credential object or dict

    Returns:
        Dict with connection_name and values fields

    """
    if hasattr(credential, 'to_dict'):
        return credential.to_dict()
    if isinstance(credential, dict):
        return credential
    # Duck-type extraction
    conn = getattr(credential, 'connection', None)
    conn_name = getattr(conn, 'name', 'unknown') if conn else 'unknown'
    values = getattr(credential, 'values', {})
    return {'connection_name': conn_name, 'values': values}


def get_credential_values_for_encryption(credential: Any) -> Dict[str, Any]:
    """Extract credential values for client-side encryption.

    This returns ONLY the credential values (no metadata) that will be
    encrypted with the server's public key before transmission.

    Args:
        credential: Credential object with values_for_encryption() or values property

    Returns:
        Dict of credential values to encrypt

    """
    if hasattr(credential, 'values_for_encryption'):
        return credential.values_for_encryption()
    # Check for dict first to avoid treating dict.values method as property
    if isinstance(credential, dict) and 'values' in credential:
        return credential['values']
    if hasattr(credential, 'values'):
        values = credential.values
        # Handle both property (returns dict) and dict-like (has items method)
        if callable(values):
            return {}  # dict.values() method, not what we want
        return dict(values) if hasattr(values, 'items') else values
    return {}


def collect_unique_connections(servers: Sequence[Any]) -> List[Any]:
    """Collect unique connections from multiple MCPServer instances.

    If two servers share the same Connection object (by name), it appears
    only once in the result. This enables single-provisioning for shared
    connections.

    Args:
        servers: List of MCPServer objects

    Returns:
        List of unique Connection objects (deduplicated by name)

    """
    seen_names: set[str] = set()
    unique: List[Any] = []

    for server in servers:
        connections = getattr(server, 'connections', {})
        # Handle both dict (MCPServer.connections) and list formats
        if isinstance(connections, dict):
            conn_list = list(connections.values())
        else:
            conn_list = list(connections) if connections else []

        for conn in conn_list:
            name = (
                getattr(conn, 'name', None)
                if hasattr(conn, 'name')
                else conn.get('name')
                if isinstance(conn, dict)
                else None
            )
            if name and name not in seen_names:
                seen_names.add(name)
                unique.append(conn)

    return unique


def match_credentials_to_connections(
    connections: Sequence[Any],
    credentials: Sequence[Any],
) -> List[tuple[Any, Any]]:
    """Match Credential objects to their Connection definitions.

    Args:
        connections: List of Connection objects
        credentials: List of Credential objects

    Returns:
        List of (connection, credential) pairs

    Raises:
        ValueError: If a connection has no matching credential

    """
    # Build lookup by connection name
    creds_by_name: Dict[str, Any] = {}
    for cred in credentials:
        if hasattr(cred, 'connection'):
            name = getattr(cred.connection, 'name', None)
        elif isinstance(cred, dict):
            name = cred.get('connection_name')
        else:
            continue
        if name:
            creds_by_name[name] = cred

    # Match connections to credentials
    pairs: List[tuple[Any, Any]] = []
    missing: List[str] = []

    for conn in connections:
        name = (
            getattr(conn, 'name', None) if hasattr(conn, 'name') else conn.get('name')
        )
        if name and name in creds_by_name:
            pairs.append((conn, creds_by_name[name]))
        elif name:
            missing.append(name)

    if missing:
        raise ValueError(
            f'Missing credentials for connections: {sorted(missing)}. '
            f'Each Connection declared in mcp_servers must have a corresponding Credential.'
        )

    return pairs


def validate_credentials_for_servers(
    servers: Sequence[Any],
    credentials: Sequence[Any],
) -> List[tuple[Any, Any]]:
    """Validate that all connections across servers have credentials.

    This is the main entry point for SDK initialization validation.
    It collects unique connections from all servers and ensures each
    has a matching Credential.

    Args:
        servers: List of MCPServer objects
        credentials: List of Credential objects

    Returns:
        List of (connection, credential) pairs ready for provisioning

    Raises:
        ValueError: If any connection lacks a credential (fail-fast at init)

    """
    connections = collect_unique_connections(servers)
    return match_credentials_to_connections(connections, credentials)


__all__ = [
    'MCPServerWireSpec',
    'serialize_mcp_servers',
    'serialize_credentials',
    'serialize_mcp_server_with_creds',
    'match_credentials_to_server',
    'build_connection_record',
    # Connection/Credential protocol
    'serialize_connection',
    'serialize_credential',
    'get_credential_values_for_encryption',
    'collect_unique_connections',
    'match_credentials_to_connections',
    'validate_credentials_for_servers',
]
