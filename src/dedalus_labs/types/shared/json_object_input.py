# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypeAlias

__all__ = ["JSONObjectInput"]

JSONObjectInput: TypeAlias = Dict[str, Optional["JSONValueInput"]]

from .json_value_input import JSONValueInput
