# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
# TODO: Temporarily using RootModel for recursive type support (Python 3.10+)

from __future__ import annotations

from typing import Dict, List, Union, Optional

from pydantic import RootModel

__all__ = ["JSONValueInput"]


class JSONValueInput(
    RootModel[Union[str, float, bool, Dict[str, Optional["JSONValueInput"]], List[Optional["JSONValueInput"]], None]]
):
    pass  # Don't include a docstring to use the upstream type's docstring


JSONValueInput.model_rebuild(_parent_namespace_depth=0)
