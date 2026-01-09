# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["MCPServerSpec"]


class MCPServerSpec(BaseModel):
    """Structured MCP server specification.

    Slug-based: {"slug": "dedalus-labs/brave-search", "name": "github-integration", "version": "v1.0.0"}
    URL-based:  {"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp", "name": "custom-server"}
    """

    name: str
    """Server instance name for credential matching."""

    credentials: Optional[Dict[str, str]] = None
    """Encrypted credential blobs keyed by connection name.

    Values are base64url ciphertext produced by the SDK (client-side encryption with
    the AS public key).
    """

    slug: Optional[str] = None
    """Marketplace identifier."""

    url: Optional[str] = None
    """Direct URL to MCP server endpoint (Pro users)."""

    version: Optional[str] = None
    """Version constraint for slug-based servers."""
