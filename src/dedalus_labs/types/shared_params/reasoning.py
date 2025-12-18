# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

__all__ = ["Reasoning"]


class ReasoningTyped(TypedDict, total=False):
    """**gpt-5 and o-series models only**

    Configuration options for
    [reasoning models](https://platform.openai.com/docs/guides/reasoning).
    """

    effort: Optional[Literal["none", "minimal", "low", "medium", "high", "xhigh"]]

    generate_summary: Optional[Literal["auto", "concise", "detailed"]]

    summary: Optional[Literal["auto", "concise", "detailed"]]


Reasoning: TypeAlias = Union[ReasoningTyped, Dict[str, object]]
