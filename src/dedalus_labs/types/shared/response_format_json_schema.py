# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ResponseFormatJSONSchema", "JSONSchema"]


class JSONSchema(BaseModel):
    name: str

    description: Optional[str] = None

    schema_: Optional[Dict[str, object]] = FieldInfo(alias="schema", default=None)
    """
    The schema for the response format, described as a JSON Schema object. Learn how
    to build JSON schemas [here](https://json-schema.org/).
    """

    strict: Optional[Dict[str, object]] = None


class ResponseFormatJSONSchema(BaseModel):
    json_schema: JSONSchema
    """Structured Outputs configuration options, including a JSON Schema."""

    type: Optional[Literal["json_schema"]] = None
