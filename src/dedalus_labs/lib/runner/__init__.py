# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Dedalus runner module."""

from __future__ import annotations

from ..utils._schemas import to_schema
from .core import DedalusRunner, MCPServersInput
from .mcp_wire import (
    MCPServerWireSpec,
    serialize_mcp_servers,
    serialize_connection,
    serialize_credential,
    get_credential_values_for_encryption,
    collect_unique_connections,
    match_credentials_to_connections,
    validate_credentials_for_servers,
)

# Encryption (requires cryptography extra)
try:
    from .encryption import (
        jwk_to_public_key,
        encrypt_credentials,
        fetch_encryption_public_key,
        fetch_encryption_public_key_sync,
        prepare_connection_payload,
    )

    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False
from .protocols import (
    MCPServerProtocol,
    MCPServerRef,
    MCPToolSpec,
    is_mcp_server,
    normalize_mcp_servers,
)
from .types import (
    JsonValue,
    Message,
    PolicyContext,
    PolicyFunction,
    PolicyInput,
    Tool,
    ToolCall,
    ToolHandler,
    ToolResult,
)

__all__ = [
    # Core
    "DedalusRunner",
    "MCPServersInput",
    # MCP protocols
    "MCPServerProtocol",
    "MCPServerRef",
    "MCPToolSpec",
    "is_mcp_server",
    "normalize_mcp_servers",
    # MCP wire format
    "MCPServerWireSpec",
    "serialize_mcp_servers",
    # Connection/Credential serialization
    "serialize_connection",
    "serialize_credential",
    "get_credential_values_for_encryption",
    "collect_unique_connections",
    "match_credentials_to_connections",
    "validate_credentials_for_servers",
    # Encryption (requires cryptography extra)
    "jwk_to_public_key",
    "encrypt_credentials",
    "fetch_encryption_public_key",
    "fetch_encryption_public_key_sync",
    "prepare_connection_payload",
    # Types
    "JsonValue",
    "Message",
    "PolicyContext",
    "PolicyFunction",
    "PolicyInput",
    "Tool",
    "ToolCall",
    "ToolHandler",
    "ToolResult",
    "to_schema",
]
