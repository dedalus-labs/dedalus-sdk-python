# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["ToolChoice", "MCPToolChoice"]


class MCPToolChoice(TypedDict, total=False):
    name: Required[str]

    server_label: Required[str]


ToolChoice: TypeAlias = Union[Literal["auto", "required", "none"], str, Dict[str, object], MCPToolChoice]
