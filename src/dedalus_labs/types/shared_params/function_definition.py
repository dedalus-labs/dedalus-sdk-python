# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["FunctionDefinition"]


class FunctionDefinition(TypedDict, total=False):
    """Schema for Function.

    Fields:
    - name (required): str
    """

    name: Required[str]
    """The name of the function to call."""
