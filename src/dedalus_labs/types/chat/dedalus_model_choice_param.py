# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .model_id import ModelID
from ..dedalus_model_param import DedalusModelParam

__all__ = ["DedalusModelChoiceParam"]

DedalusModelChoiceParam: TypeAlias = Union[ModelID, DedalusModelParam]
