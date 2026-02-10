# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["VoiceIDsOrCustomVoice"]


class VoiceIDsOrCustomVoice(TypedDict, total=False):
    """Custom voice reference.

    Fields:
    - id (required): str
    """

    id: Required[str]
    """The custom voice ID, e.g. `voice_1234`."""
