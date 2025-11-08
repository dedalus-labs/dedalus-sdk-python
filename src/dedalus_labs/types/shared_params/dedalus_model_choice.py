# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .dedalus_model import DedalusModel
from ..chat.model_id import ModelID

__all__ = ["DedalusModelChoice"]

DedalusModelChoice: TypeAlias = Union[ModelID, DedalusModel]
