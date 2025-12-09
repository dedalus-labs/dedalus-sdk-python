# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .mcp_server_spec import MCPServerSpec

__all__ = ["MCPServerInput"]

MCPServerInput: TypeAlias = Union[str, MCPServerSpec]
