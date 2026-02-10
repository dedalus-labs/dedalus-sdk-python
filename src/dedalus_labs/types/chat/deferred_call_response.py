# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["DeferredCallResponse"]


class DeferredCallResponse(BaseModel):
    """Server-side call blocked until pending client calls complete.

    Carries full spec for stateless resumption on subsequent turns.
    """

    id: str
    """Unique identifier for this deferred call."""

    name: str
    """Name of the tool."""

    arguments: Optional["JSONObjectInput"] = None
    """Input arguments for the tool call."""

    blocked_by: Optional[List[str]] = None
    """IDs of pending client calls blocking this call."""

    dependencies: Optional[List[str]] = None
    """IDs of calls this depends on."""

    venue: Optional[str] = None
    """Execution venue (server or client)."""


from ..shared.json_object_input import JSONObjectInput
