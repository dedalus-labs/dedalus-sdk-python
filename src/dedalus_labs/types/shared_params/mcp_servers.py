# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import TypeAlias

from .mcp_server_param import MCPServerParam

__all__ = ["MCPServers", "MCPServerInput"]

MCPServerInput: TypeAlias = Union[str, MCPServerParam]

MCPServers: TypeAlias = List[MCPServerInput]
