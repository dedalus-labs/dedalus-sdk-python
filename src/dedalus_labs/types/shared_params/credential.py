# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypedDict

__all__ = ["Credential"]


class Credential(TypedDict, total=False):
    """Credential for MCP server authentication.

    Passed at endpoint level (e.g., chat.completions.create) and matched
    to MCP servers by connection name. Wire format matches dedalus_mcp.Credential.to_dict().
    """

    connection_name: Required[str]
    """Connection name. Must match a connection in MCPServer.connections."""

    values: Required[Dict[str, Union[str, int, bool]]]
    """Credential values. Keys are credential field names, values are the secrets."""
