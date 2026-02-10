# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["DeferredCallResponseParam"]


class DeferredCallResponseParam(TypedDict, total=False):
    """Server-side call blocked until pending client calls complete.

    Carries full spec for stateless resumption on subsequent turns.
    """

    id: Required[str]
    """Unique identifier for this deferred call."""

    name: Required[str]
    """Name of the tool."""

    arguments: "JSONObjectInput"
    """Input arguments for the tool call."""

    blocked_by: SequenceNotStr[str]
    """IDs of pending client calls blocking this call."""

    dependencies: SequenceNotStr[str]
    """IDs of calls this depends on."""

    venue: str
    """Execution venue (server or client)."""


from ..shared_params.json_object_input import JSONObjectInput
