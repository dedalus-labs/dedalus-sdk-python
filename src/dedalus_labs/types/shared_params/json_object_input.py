# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypeAliasType

from ... import _compat

__all__ = ["JSONObjectInput"]

from .json_value_input import JSONValueInput

if _compat.PYDANTIC_V1:
    JSONObjectInput = Dict[str, JSONValueInput]
else:
    JSONObjectInput = TypeAliasType("JSONObjectInput", Dict[str, JSONValueInput])
