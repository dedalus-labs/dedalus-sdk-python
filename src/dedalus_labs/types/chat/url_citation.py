# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["URLCitation"]


class URLCitation(BaseModel):
    """A URL citation when using web search.

    Fields:
    - end_index (required): int
    - start_index (required): int
    - url (required): str
    - title (required): str
    """

    end_index: int
    """The index of the last character of the URL citation in the message."""

    start_index: int
    """The index of the first character of the URL citation in the message."""

    title: str
    """The title of the web resource."""

    url: str
    """The URL of the web resource."""
