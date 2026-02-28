# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["VoiceIDsOrCustomVoice"]


class VoiceIDsOrCustomVoice(BaseModel):
    """Custom voice reference.

    Fields:
    - id (required): str
    """

    id: str
    """The custom voice ID, e.g. `voice_1234`."""
