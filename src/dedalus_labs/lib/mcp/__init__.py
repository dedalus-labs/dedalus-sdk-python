# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP server integration utilities."""

from .protocols import (
    CredentialProtocol,
    MCPServerProtocol,
    MCPServerRef,
    MCPServerWithCredsProtocol,
    MCPToolSpec,
    is_mcp_server,
    normalize_mcp_servers,
)
from .request import (
    EncryptedCredentials,
    prepare_mcp_request,
    prepare_mcp_request_sync,
)
from .wire import (
    MCPServerWireSpec,
    collect_unique_connections,
    match_credentials_to_connections,
    serialize_connection,
    serialize_mcp_servers,
    validate_credentials_for_servers,
)

__all__ = [
    # Protocols
    "CredentialProtocol",
    "MCPServerProtocol",
    "MCPServerRef",
    "MCPServerWithCredsProtocol",
    "MCPToolSpec",
    "is_mcp_server",
    "normalize_mcp_servers",
    # Wire format
    "MCPServerWireSpec",
    "collect_unique_connections",
    "match_credentials_to_connections",
    "serialize_connection",
    "serialize_mcp_servers",
    "validate_credentials_for_servers",
    # Request preparation
    "EncryptedCredentials",
    "prepare_mcp_request",
    "prepare_mcp_request_sync",
]
