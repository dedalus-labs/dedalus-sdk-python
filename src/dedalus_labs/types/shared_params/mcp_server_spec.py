# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["MCPServerSpec"]


class MCPServerSpec(TypedDict, total=False):
    """Structured MCP server specification.

    Slug-based: {"slug": "dedalus-labs/brave-search", "name": "github-integration", "version": "v1.0.0"}
    URL-based:  {"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp", "name": "custom-server"}
    """

    name: Required[str]
    """Server instance name for credential matching."""

    credentials: Optional[Dict[str, str]]
    """Encrypted credential blobs keyed by connection name.

    Values are base64url ciphertext produced by the SDK (client-side encryption with
    the AS public key).
    """

    slug: Optional[str]
    """Marketplace identifier."""

    url: Optional[str]
    """Direct URL to MCP server endpoint (Pro users)."""

    version: Optional[str]
    """Version constraint for slug-based servers."""
