# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union

from ..._models import BaseModel

__all__ = ["Credential"]


class Credential(BaseModel):
    """Credential for MCP server authentication.

    Passed at endpoint level (e.g., chat.completions.create) and matched
    to MCP servers by connection name. Wire format matches dedalus_mcp.Credential.to_dict().
    """

    connection_name: str
    """Connection name. Must match a connection in MCPServer.connections."""

    values: Dict[str, Union[str, int, bool]]
    """Credential values. Keys are credential field names, values are the secrets."""
