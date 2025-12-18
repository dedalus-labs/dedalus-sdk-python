# Copyright (c) 2025 Dedalus Labs, Inc.
# SPDX-License-Identifier: MIT

"""Tests for RootModel construction in construct_type.

These tests verify that Pydantic RootModel types are correctly constructed
when deserializing API responses, with the value properly placed in `.root`.
"""

from typing import Any, Dict, List, Union

import pytest

from dedalus_labs._compat import PYDANTIC_V1
from dedalus_labs._models import construct_type, BaseModel

if not PYDANTIC_V1:
    from pydantic import RootModel


@pytest.mark.skipif(PYDANTIC_V1, reason="RootModel is only available in Pydantic v2")
class TestRootModelConstruction:
    """Test construct_type correctly handles RootModel types."""

    def test_simple_value(self) -> None:
        """RootModel with a simple string value."""
        class JSONValue(RootModel[Union[str, float, bool, None]]):
            pass

        m = construct_type(value="hello", type_=JSONValue)
        assert isinstance(m, JSONValue)
        assert m.root == "hello"

    def test_dict_value(self) -> None:
        """RootModel wrapping a dict."""
        class JSONObject(RootModel[Dict[str, Any]]):
            pass

        m = construct_type(value={"key": "value", "num": 42}, type_=JSONObject)
        assert isinstance(m, JSONObject)
        assert m.root == {"key": "value", "num": 42}

    def test_list_value(self) -> None:
        """RootModel wrapping a list."""
        class JSONArray(RootModel[List[Any]]):
            pass

        m = construct_type(value=[1, "two", True], type_=JSONArray)
        assert isinstance(m, JSONArray)
        assert m.root == [1, "two", True]

    def test_nested_in_basemodel(self) -> None:
        """RootModel as a field in a BaseModel."""
        class JSONObject(RootModel[Dict[str, Any]]):
            pass

        class Container(BaseModel):
            arguments: JSONObject

        container = construct_type(
            value={"arguments": {"per_page": 100, "nested": {"deep": "value"}}},
            type_=Container,
        )
        assert isinstance(container, Container)
        assert isinstance(container.arguments, JSONObject)
        assert container.arguments.root == {"per_page": 100, "nested": {"deep": "value"}}

    def test_list_of_rootmodel(self) -> None:
        """List containing RootModel instances."""
        class JSONValue(RootModel[Union[str, int, Dict[str, Any], None]]):
            pass

        class Container(BaseModel):
            items: List[JSONValue]

        container = construct_type(
            value={"items": ["a", 1, {"key": "val"}]},
            type_=Container,
        )
        assert isinstance(container, Container)
        assert len(container.items) == 3
        assert all(isinstance(item, JSONValue) for item in container.items)
        assert container.items[0].root == "a"
        assert container.items[1].root == 1
        assert container.items[2].root == {"key": "val"}

    def test_recursive_rootmodel(self) -> None:
        """Recursive RootModel type (like JSONValue)."""
        # This mimics our actual JSONValueOutput type
        class JSONValue(
            RootModel[Union[str, float, bool, Dict[str, "JSONValue"], List["JSONValue"], None]]
        ):
            pass

        JSONValue.model_rebuild()

        m = construct_type(value={"nested": {"deep": "value"}}, type_=JSONValue)
        assert isinstance(m, JSONValue)
        # The root should be the raw dict (construct_type doesn't recursively wrap inner dicts)
        assert m.root == {"nested": {"deep": "value"}}
