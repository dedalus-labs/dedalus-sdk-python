# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import TypeAlias

from .model_id import ModelID
from ..shared_params.dedalus_model import DedalusModel

__all__ = ["ModelsParam", "DedalusModelChoice"]

DedalusModelChoice: TypeAlias = Union[ModelID, DedalusModel]

ModelsParam: TypeAlias = List[DedalusModelChoice]
