# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel
from .url_citation import URLCitation

__all__ = ["Annotation"]


class Annotation(BaseModel):
    """A URL citation when using web search.

    Fields:
    - type (required): Literal["url_citation"]
    - url_citation (required): UrlCitation
    """

    type: Literal["url_citation"]
    """The type of the URL citation. Always `url_citation`."""

    url_citation: URLCitation
    """A URL citation when using web search."""
