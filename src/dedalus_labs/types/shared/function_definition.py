# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["FunctionDefinition"]


class FunctionDefinition(BaseModel):
    """Schema for Function.

    Fields:
    - name (required): str
    """

    name: str
    """The name of the function to call."""
