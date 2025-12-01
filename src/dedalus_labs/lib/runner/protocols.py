# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Structural protocols for MCP server integration.

Enables the Dedalus SDK to accept OpenMCP servers as a parameter.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, Union, Optional, Protocol, Sequence, runtime_checkable

# --- Type Aliases ------------------------------------------------------------

MCPServerRef = str  # Slug ("org/server") or URL

# --- Protocols ---------------------------------------------------------------


@runtime_checkable
class MCPServerProtocol(Protocol):
    """Structural protocol for MCP servers.

    OpenMCP's MCPServer naturally conforms. The @runtime_checkable decorator
    enables isinstance() checks at runtime.
    """

    @property
    def name(self) -> str: ...

    @property
    def url(self) -> Optional[str]: ...

    def serve(self, *args: Any, **kwargs: Any) -> Any: ...


@runtime_checkable
class MCPToolSpec(Protocol):
    """Duck-typed interface for tool specifications."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> Optional[str]: ...

    @property
    def input_schema(self) -> Dict[str, Any]: ...


# --- Helpers -----------------------------------------------------------------


def is_mcp_server(obj: Any) -> bool:
    """Check if obj satisfies MCPServerProtocol."""
    return isinstance(obj, MCPServerProtocol)


def normalize_mcp_servers(
    servers: Union[MCPServerRef, Sequence[Union[MCPServerRef, MCPServerProtocol]], MCPServerProtocol, None],
) -> Tuple[List[MCPServerRef], List[MCPServerProtocol]]:
    """Split into (string refs, server objects). Caller checks .url to know if serve() is needed."""
    if servers is None:
        return [], []
    if isinstance(servers, str):
        return [servers], []
    if is_mcp_server(servers):
        return [], [servers]  # type: ignore[list-item]

    refs: List[MCPServerRef] = []
    objects: List[MCPServerProtocol] = []
    for item in servers:
        if isinstance(item, str):
            refs.append(item)
        elif is_mcp_server(item):
            objects.append(item)
        else:
            refs.append(str(item))
    return refs, objects
