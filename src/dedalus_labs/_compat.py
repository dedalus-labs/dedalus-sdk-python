from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar, Callable, overload
from datetime import date, datetime
from typing_extensions import Self, Literal

import pydantic
from pydantic.fields import FieldInfo
from pydantic import ConfigDict
from pydantic.v1.typing import (
    get_args,
    is_union,
    get_origin,
    is_typeddict,
    is_literal_type,
)
from pydantic.v1.datetime_parse import parse_date, parse_datetime

from ._types import IncEx

_T = TypeVar("_T")
_ModelT = TypeVar("_ModelT", bound=pydantic.BaseModel)

# Pyright incorrectly reports some of our functions as overriding a method when they don't
# pyright: reportIncompatibleMethodOverride=false


# Pydantic v2 methods
def parse_obj(model: type[_ModelT], value: object) -> _ModelT:
    return model.model_validate(value)


def field_is_required(field: FieldInfo) -> bool:
    return field.is_required()


def field_get_default(field: FieldInfo) -> Any:
    from pydantic_core import PydanticUndefined
    
    value = field.get_default()
    if value == PydanticUndefined:
        return None
    return value


def field_outer_type(field: FieldInfo) -> Any:
    return field.annotation


def get_model_config(model: type[pydantic.BaseModel]) -> Any:
    return model.model_config


def get_model_fields(model: type[pydantic.BaseModel]) -> dict[str, FieldInfo]:
    return model.model_fields


def model_copy(model: _ModelT, *, deep: bool = False) -> _ModelT:
    return model.model_copy(deep=deep)


def model_json(model: pydantic.BaseModel, *, indent: int | None = None) -> str:
    return model.model_dump_json(indent=indent)


def model_dump(
    model: pydantic.BaseModel,
    *,
    exclude: IncEx | None = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    warnings: bool = True,
    mode: Literal["json", "python"] = "python",
) -> dict[str, Any]:
    return model.model_dump(
        mode=mode,
        exclude=exclude,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        warnings=warnings,
    )


def model_parse(model: type[_ModelT], data: Any) -> _ModelT:
    return model.model_validate(data)


# In Pydantic v2, GenericModel is just BaseModel
class GenericModel(pydantic.BaseModel):
    pass


# cached properties
if TYPE_CHECKING:
    cached_property = property

    # we define a separate type (copied from typeshed)
    # that represents that `cached_property` is `set`able
    # at runtime, which differs from `@property`.
    #
    # this is a separate type as editors likely special case
    # `@property` and we don't want to cause issues just to have
    # more helpful internal types.

    class typed_cached_property(Generic[_T]):
        func: Callable[[Any], _T]
        attrname: str | None

        def __init__(self, func: Callable[[Any], _T]) -> None: ...

        @overload
        def __get__(self, instance: None, owner: type[Any] | None = None) -> Self: ...

        @overload
        def __get__(self, instance: object, owner: type[Any] | None = None) -> _T: ...

        def __get__(self, instance: object, owner: type[Any] | None = None) -> _T | Self:
            raise NotImplementedError()

        def __set_name__(self, owner: type[Any], name: str) -> None: ...

        # __set__ is not defined at runtime, but @cached_property is designed to be settable
        def __set__(self, instance: object, value: _T) -> None: ...
else:
    from functools import cached_property as cached_property

    typed_cached_property = cached_property
