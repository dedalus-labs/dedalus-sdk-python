# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ResponseFormatJSONSchema", "JSONSchema"]


class JSONSchema(TypedDict, total=False):
    name: Required[str]

    description: Optional[str]

    schema: Optional[Dict[str, object]]
    """
    The schema for the response format, described as a JSON Schema object. Learn how
    to build JSON schemas [here](https://json-schema.org/).
    """

    strict: Optional[Dict[str, object]]


class ResponseFormatJSONSchema(TypedDict, total=False):
    json_schema: Required[JSONSchema]
    """Structured Outputs configuration options, including a JSON Schema."""

    type: Literal["json_schema"]
