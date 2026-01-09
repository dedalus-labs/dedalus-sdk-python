# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypeAliasType

__all__ = ["JSONObjectInput"]

from .json_value_input import JSONValueInput

JSONObjectInput = TypeAliasType("JSONObjectInput", Dict[str, Optional[JSONValueInput]])
