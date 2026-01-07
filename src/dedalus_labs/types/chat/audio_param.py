# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AudioParam"]


class AudioParam(TypedDict, total=False):
    """
    Data about a previous audio response from the model.
    [Learn more](https://platform.openai.com/docs/guides/audio).

    Fields:
    - id (required): str
    """

    id: Required[str]
    """Unique identifier for a previous audio response from the model."""
