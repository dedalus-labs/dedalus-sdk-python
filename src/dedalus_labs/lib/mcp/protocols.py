# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Structural protocols for MCP server integration."""

from __future__ import annotations

from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
    Optional,
    Protocol,
    Sequence,
    runtime_checkable,
)

from typing_extensions import TypeGuard


# --- Type Aliases ------------------------------------------------------------

MCPServerRef = str  # Slug ("org/server") or URL

# --- Protocols ---------------------------------------------------------------


@runtime_checkable
class CredentialProtocol(Protocol):
    """Protocol for a single credential binding (e.g., SecretValues)."""

    @property
    def connection(self) -> Any:
        """Connection this credential binds to (must have .name)."""
        ...

    def values_for_encryption(self) -> Dict[str, Any]:
        """Return CredentialEnvelope for client-side encryption."""
        ...


@runtime_checkable
class ToolsServiceProtocol(Protocol):
    """Protocol for tools service from MCPServer."""

    @property
    def _tool_specs(self) -> Dict[str, Any]: ...


@runtime_checkable
class MCPServerProtocol(Protocol):
    """Structural protocol for MCP servers."""

    @property
    def name(self) -> str: ...

    @property
    def url(self) -> Optional[str]: ...

    def serve(self, *args: Any, **kwargs: Any) -> Any: ...


@runtime_checkable
class MCPServerWithCredsProtocol(Protocol):
    """Extended protocol for MCPServer with credential bindings.

    Used for connection provisioning flow where servers need credentials.
    """

    @property
    def name(self) -> str: ...

    @property
    def credentials(self) -> Optional[CredentialsProtocol]: ...

    @property
    def connection(self) -> Optional[str]: ...

    @property
    def tools(self) -> ToolsServiceProtocol: ...


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


def is_mcp_server(obj: Any) -> TypeGuard[MCPServerProtocol]:
    """Check if obj satisfies MCPServerProtocol."""
    return isinstance(obj, MCPServerProtocol)


def normalize_mcp_servers(
    servers: Union[
        MCPServerRef,
        Sequence[Union[MCPServerRef, MCPServerProtocol]],
        MCPServerProtocol,
        None,
    ],
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
