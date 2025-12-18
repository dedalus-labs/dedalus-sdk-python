# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypeAlias

__all__ = ["JSONObjectOutput"]

JSONObjectOutput: TypeAlias = Dict[str, Optional["JSONValueOutput"]]

from .json_value_output import JSONValueOutput
