# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["MCPServerParam"]


class MCPServerParam(TypedDict, total=False):
    slug: Optional[str]
    """Marketplace slug."""

    url: Optional[str]
    """Direct URL to MCP server endpoint."""

    version: Optional[str]
    """Version constraint for slug-based servers."""
