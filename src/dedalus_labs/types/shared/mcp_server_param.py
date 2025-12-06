# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["MCPServerParam", "Credentials", "CredentialsBindingSpec"]


class CredentialsBindingSpec(BaseModel):
    name: str
    """Environment variable name or source identifier."""

    cast: Optional[str] = None
    """Type to cast value to (e.g., 'int', 'bool')."""

    default: Optional[object] = None
    """Default value if source not set."""

    optional: Optional[bool] = None
    """If true, missing value is allowed."""


Credentials: TypeAlias = Union[str, CredentialsBindingSpec]


class MCPServerParam(BaseModel):
    connection: Optional[str] = None
    """Connection name for credential matching.

    Must match a key in the client's credentials list.
    """

    credentials: Optional[Dict[str, Credentials]] = None
    """Schema declaring what credentials are needed.

    Maps field names to their bindings (e.g., env var names).
    """

    slug: Optional[str] = None
    """Marketplace slug."""

    url: Optional[str] = None
    """Direct URL to MCP server endpoint."""

    version: Optional[str] = None
    """Version constraint for slug-based servers."""
