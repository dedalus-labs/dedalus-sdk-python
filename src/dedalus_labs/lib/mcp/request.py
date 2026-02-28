# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP request preparation.

This module handles the client-side preparation of MCP requests:
1. Serializes MCPServer objects to wire format (dicts/strings)
2. Deep copies to protect retry logic from mutation side effects
3. Encrypts credentials client-side before transmission
"""

from __future__ import annotations

import copy
import logging
from typing import Any, Dict, List, Optional, Sequence
from dataclasses import dataclass

from dedalus_labs.types.shared_params.mcp_servers import MCPServerItem
from dedalus_labs.types.shared_params.mcp_server_spec import MCPServerSpec

from .wire import serialize_mcp_servers, slug_to_connection_name
from ..crypto import encrypt_credentials, fetch_encryption_key, fetch_encryption_key_sync
from .protocols import CredentialProtocol

logger = logging.getLogger(__name__)

__all__ = [
    "prepare_mcp_request",
    "prepare_mcp_request_sync",
    "EncryptedCredentials",
]


@dataclass(frozen=True)
class EncryptedCredentials:
    """Map of connection names to encrypted envelopes (base64url).

    Instantiate with connection names as keyword arguments:
        >>> EncryptedCredentials(foo="encrypted...", bar="encrypted...")
    """

    entries: Dict[str, str]

    def __init__(self, **kwargs: str) -> None:
        object.__setattr__(self, "entries", dict(kwargs))

    def to_dict(self) -> Dict[str, str]:
        """Return the underlying dict for wire serialization."""
        return self.entries


# --- Request Preparation ---


async def prepare_mcp_request(
    data: Dict[str, Any],
    as_url: Optional[str],
    http_client: Any,
) -> Dict[str, Any]:
    """Serialize mcp_servers, deepcopy, and encrypt credentials.

    Args:
        data: Request body dict (modified in place before copy).
        as_url: Authorization server URL for fetching encryption key.
        http_client: httpx.AsyncClient for key fetch.

    Returns:
        A new dict with serialized servers and encrypted credentials.

    """
    # Serialize MCP servers, if provided.
    servers = data.get("mcp_servers")
    if servers is not None:
        data["mcp_servers"] = serialize_mcp_servers(servers)

    # Make a copy to avoid mutation side effects related to SDK retry logic.
    data = copy.deepcopy(data)
    credentials = data.get("credentials")

    # If credentials are provided, encrypt them on the client side
    # and transport them along with the MCP servers.
    if credentials and servers and as_url:
        try:
            public_key = await fetch_encryption_key(http_client, as_url)
            encrypted = _encrypt_credentials(credentials, public_key)
            if encrypted:
                data["mcp_servers"] = _embed_credentials(data["mcp_servers"], encrypted)
                data.pop("credentials", None)
        except ImportError as err:
            msg = "The `cryptography` package is required for authentication. Install: `uv pip install 'dedalus-labs[auth]'`"
            raise ImportError(msg) from err

    return data


def prepare_mcp_request_sync(
    data: Dict[str, Any],
    as_url: Optional[str],
    http_client: Any,
) -> Dict[str, Any]:
    """Sync version of prepare_mcp_request.

    Args:
        data: Request body dict (modified in place before copy).
        as_url: Authorization server URL for fetching encryption key.
        http_client: httpx.Client for key fetch.

    Returns:
        A new dict with serialized servers and encrypted credentials.

    """
    # Serialize MCP servers, if provided.
    servers = data.get("mcp_servers")
    if servers is not None:
        data["mcp_servers"] = serialize_mcp_servers(servers)

    # Make a copy to avoid mutation side effects related to SDK retry logic.
    data = copy.deepcopy(data)
    credentials = data.get("credentials")

    # If credentials are provided, encrypt them on the client side
    # and transport them along with the MCP servers.
    if credentials and servers and as_url:
        try:
            public_key = fetch_encryption_key_sync(http_client, as_url)
            encrypted = _encrypt_credentials(credentials, public_key)
            if encrypted:
                data["mcp_servers"] = _embed_credentials(data["mcp_servers"], encrypted)
                data.pop("credentials", None)
        except ImportError as err:
            msg = "cryptography required for credentials. Install: uv pip install 'dedalus-labs[auth]'"
            raise ImportError(msg) from err

    return data


# --- Internal Helpers ---


def _encrypt_credentials(
    credentials: Sequence[CredentialProtocol],
    public_key: Any,
) -> EncryptedCredentials:
    """Encrypt each credential.

    Args:
        credentials: Credential objects implementing CredentialProtocol.
        public_key: RSA public key from fetch_encryption_key.

    Returns:
        EncryptedCredentials with connection names mapped to base64url envelopes.

    """
    encrypted = {
        cred.connection.name: encrypt_credentials(public_key, cred.values_for_encryption()) for cred in credentials
    }
    return EncryptedCredentials(**encrypted)


def _credentials_for_server(
    name: str,
    all_creds: Dict[str, str],
) -> Optional[Dict[str, str]]:
    """Return the subset of *all_creds* that belongs to *name*, or None."""
    conn = slug_to_connection_name(name)
    blob = all_creds.get(conn)
    return {conn: blob} if blob is not None else None


def _embed_credentials(
    servers: List[MCPServerItem],
    encrypted: EncryptedCredentials,
) -> List[MCPServerSpec]:
    """Embed encrypted credentials into each server spec.

    Each server receives only its own credentials, matched by connection name
    via :func:`~dedalus_labs.lib.mcp.wire.slug_to_connection_name`.

    Args:
        servers: Serialized MCP servers (slug strings or spec dicts).
        encrypted: EncryptedCredentials instance.

    Returns:
        List of MCPServerSpec dicts with per-server credentials embedded.

    """
    all_creds = encrypted.to_dict()
    result: List[MCPServerSpec] = []

    for server in servers:
        if isinstance(server, str):
            creds = _credentials_for_server(server, all_creds)
            if server.startswith(("http://", "https://")):
                result.append({"url": server, "name": server, "credentials": creds})
            else:
                result.append({"slug": server, "name": server, "credentials": creds})
        elif isinstance(server, dict):
            name = server.get("name") or server.get("slug") or server.get("url") or ""
            creds = _credentials_for_server(name, all_creds)
            result.append({**server, "name": name, "credentials": creds})

    return result
