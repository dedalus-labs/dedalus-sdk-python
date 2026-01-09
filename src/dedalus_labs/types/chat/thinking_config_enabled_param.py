# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ThinkingConfigEnabledParam"]


class ThinkingConfigEnabledParam(TypedDict, total=False):
    """Schema for ThinkingConfigEnabled.

    Fields:
    - budget_tokens (required): int
    - type (required): Literal["enabled"]
    """

    budget_tokens: Required[int]
    """Determines how many tokens Claude can use for its internal reasoning process.

    Larger budgets can enable more thorough analysis for complex problems, improving
    response quality.

    Must be ≥1024 and less than `max_tokens`.

    See
    [extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking)
    for details.
    """

    type: Required[Literal["enabled"]]
