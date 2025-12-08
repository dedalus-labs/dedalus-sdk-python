# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["MCPServerParam", "Credentials", "CredentialsBindingSpec"]


class CredentialsBindingSpec(TypedDict, total=False):
    """Detailed credential binding with options.

    Used when a binding needs default values, optional flags, or type casting.
    """

    name: Required[str]
    """Environment variable name or source identifier."""

    cast: Optional[str]
    """Type to cast value to (e.g., 'int', 'bool')."""

    default: object
    """Default value if source not set."""

    optional: bool
    """If true, missing value is allowed."""


Credentials: TypeAlias = Union[str, CredentialsBindingSpec]


class MCPServerParam(TypedDict, total=False):
    """Structured MCP server parameter.

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

    slug: Optional[str]
    """Marketplace slug."""

    url: Optional[str]
    """Direct URL to MCP server endpoint."""

    version: Optional[str]
    """Version constraint for slug-based servers."""
