# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""MCP server wire format for SDK-to-API comms."""

from __future__ import annotations

from typing import Any, Dict, List, Union, Optional, Sequence

from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

# --- Pydantic Models ---------------------------------------------------------


class MCPServerWireSpec(BaseModel):
    """MCP server spec for API transmission. Either slug or url, not both."""

    model_config = ConfigDict(extra="forbid")

    slug: Optional[str] = Field(default=None, pattern=r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$")
    version: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def validate_slug_or_url(self) -> "MCPServerWireSpec":
        has_slug = self.slug is not None
        has_url = self.url is not None

        if not has_slug and not has_url:
            raise ValueError("requires either 'slug' or 'url'")
        if has_slug and has_url:
            raise ValueError("cannot have both 'slug' and 'url'")
        if has_slug and self.version and "@" in self.slug:
            raise ValueError("cannot specify both 'version' field and version in slug")

        return self

    @field_validator("url")
    @classmethod
    def validate_url_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not v.startswith(("http://", "https://")):
            raise ValueError(f"URL must start with http:// or https://, got: {v}")
        return v

    def to_wire(self) -> Union[str, Dict[str, Any]]:
        """Simple slugs become strings, everything else becomes a dict."""
        if self.slug and not self.version:
            return self.slug
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_slug(cls, slug: str, version: Optional[str] = None) -> "MCPServerWireSpec":
        if "@" in slug and version is None:
            slug, version = slug.rsplit("@", 1)
        return cls(slug=slug, version=version)

    @classmethod
    def from_url(cls, url: str) -> "MCPServerWireSpec":
        return cls(url=url)


# --- Serialization -----------------------------------------------------------


def serialize_mcp_servers(
    servers: Union[str, Sequence[Union[str, Any]], Any, None],
) -> List[Union[str, Dict[str, Any]]]:
    """Convert mcp_servers to API wire format. Handles strings, objects, or sequences."""
    from .protocols import is_mcp_server

    if servers is None:
        return []
    if isinstance(servers, str):
        return [_serialize_single(servers)]
    if is_mcp_server(servers):
        return [_serialize_single(servers)]
    return [_serialize_single(item) for item in servers]


def _serialize_single(item: Union[str, Any]) -> Union[str, Dict[str, Any]]:
    from .protocols import is_mcp_server

    if isinstance(item, str):
        if item.startswith(("http://", "https://")):
            return item
        if "@" in item:
            slug, version = item.rsplit("@", 1)
            return MCPServerWireSpec.from_slug(slug, version).to_wire()
        return item

    if is_mcp_server(item):
        url = getattr(item, "url", None)
        if url is None:
            name = getattr(item, "name", "unknown")
            raise ValueError(f"MCP server '{name}' has no URL. Call serve() first or use a slug instead.")
        return MCPServerWireSpec.from_url(url).to_wire()

    if isinstance(item, dict):
        return MCPServerWireSpec.model_validate(item).to_wire()

    return str(item)


__all__ = [
    "MCPServerWireSpec",
    "serialize_mcp_servers",
]
