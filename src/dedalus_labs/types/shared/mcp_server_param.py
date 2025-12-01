# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["MCPServerParam"]


class MCPServerParam(BaseModel):
    slug: Optional[str] = None
    """Marketplace slug."""

    url: Optional[str] = None
    """Direct URL to MCP server endpoint."""

    version: Optional[str] = None
    """Version constraint for slug-based servers."""
