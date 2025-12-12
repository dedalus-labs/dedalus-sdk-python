# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel
from .credentials_binding_spec import CredentialsBindingSpec

__all__ = ["MCPServerSpec", "Credentials"]

Credentials: TypeAlias = Union[str, CredentialsBindingSpec]


class MCPServerSpec(BaseModel):
    """Structured MCP server specification.

    Slug-based: {"slug": "dedalus-labs/brave-search", "version": "v1.0.0"}
    URL-based:  {"url": "https://mcp.dedaluslabs.ai/acme/my-server/mcp"}
    """

    connection: Optional[str] = None
    """Connection name for credential matching.

    Must match a key in the client's credentials list.
    """

    credentials: Optional[Dict[str, Credentials]] = None
    """Schema declaring what credentials are needed.

    Maps field names to their bindings (e.g., env var names).
    """

    encrypted_credentials: Optional[Dict[str, str]] = None
    """Client-encrypted credential values.

    Maps connection names to encrypted envelopes.
    """

    slug: Optional[str] = None
    """Marketplace slug."""

    url: Optional[str] = None
    """Direct URL to MCP server endpoint."""

    version: Optional[str] = None
    """Version constraint for slug-based servers."""
