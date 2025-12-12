# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP server integration utilities."""

from .protocols import (
    MCPServerProtocol,
    MCPServerRef,
    MCPServerWithCredsProtocol,
    MCPToolSpec,
    is_mcp_server,
    normalize_mcp_servers,
)
from .wire import (
    MCPServerWireSpec,
    serialize_mcp_servers,
    serialize_connection,
    serialize_credential,
    get_credential_values_for_encryption,
    collect_unique_connections,
    match_credentials_to_connections,
    validate_credentials_for_servers,
)

__all__ = [
    # Protocols
    "MCPServerProtocol",
    "MCPServerRef",
    "MCPServerWithCredsProtocol",
    "MCPToolSpec",
    "is_mcp_server",
    "normalize_mcp_servers",
    # Wire format
    "MCPServerWireSpec",
    "serialize_mcp_servers",
    "serialize_connection",
    "serialize_credential",
    "get_credential_values_for_encryption",
    "collect_unique_connections",
    "match_credentials_to_connections",
    "validate_credentials_for_servers",
]
