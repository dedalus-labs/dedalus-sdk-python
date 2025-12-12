# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import TypeAlias, TypedDict

from .credentials_binding_spec import CredentialsBindingSpec

__all__ = ["MCPServerSpec", "Credentials"]

Credentials: TypeAlias = Union[str, CredentialsBindingSpec]


class MCPServerSpec(TypedDict, total=False):
    """Structured MCP server specification.

    Slug-based: {"slug": "dedalus-labs/brave-search", "version": "v1.0.0"}
    URL-based:  {"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp"}
    """

    connection: Optional[str]
    """Connection name for credential matching.

    Must match a key in the client's credentials list.
    """

    credentials: Optional[Dict[str, Credentials]]
    """Schema declaring what credentials are needed.

    Maps field names to their bindings (e.g., env var names).
    """

    encrypted_credentials: Optional[Dict[str, str]]
    """Client-encrypted credential values.

    Maps connection names to encrypted envelopes.
    """

    slug: Optional[str]
    """Marketplace slug."""

    url: Optional[str]
    """Direct URL to MCP server endpoint."""

    version: Optional[str]
    """Version constraint for slug-based servers."""
