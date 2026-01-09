# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import TypeAlias

from .mcp_server_spec import MCPServerSpec

__all__ = ["MCPServers", "MCPServerItem"]

MCPServerItem: TypeAlias = Union[str, MCPServerSpec]

MCPServers: TypeAlias = List[MCPServerItem]
