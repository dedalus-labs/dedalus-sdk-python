# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["ToolChoice", "MCPToolChoice"]


class MCPToolChoice(BaseModel):
    name: str

    server_label: str


ToolChoice: TypeAlias = Union[Literal["auto", "required", "none"], str, Dict[str, object], MCPToolChoice, None]
