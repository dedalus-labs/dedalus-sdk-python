# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = ["ReasoningParam"]


class ReasoningParamTyped(TypedDict, total=False):
    effort: Optional[Literal["minimal", "low", "medium", "high"]]

    generate_summary: Optional[Literal["auto", "concise", "detailed"]]

    summary: Optional[Literal["auto", "concise", "detailed"]]


ReasoningParam: TypeAlias = Union[ReasoningParamTyped, Dict[str, object]]
