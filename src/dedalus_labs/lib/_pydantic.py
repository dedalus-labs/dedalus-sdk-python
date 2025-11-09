from __future__ import annotations

import inspect
from typing import Any, TypeVar
from typing_extensions import TypeGuard

import pydantic

from .._types import NOT_GIVEN
from .._utils import is_dict as _is_dict, is_list
from .._compat import PYDANTIC_V1, model_json_schema

_T = TypeVar("_T")


class SchemaError(RuntimeError):
    """Raised when schema cannot be generated or normalized."""


def to_strict_json_schema(model: type[pydantic.BaseModel] | pydantic.TypeAdapter[Any]) -> dict[str, Any]:
    """Convert Pydantic model to strict JSON schema for LLM structured outputs."""
    if inspect.isclass(model) and is_basemodel_type(model):
        schema = model_json_schema(model)
    elif (not PYDANTIC_V1) and isinstance(model, pydantic.TypeAdapter):
        schema = model.json_schema()
    else:
        raise TypeError(f"Non BaseModel types are only supported with Pydantic v2 - {model}")

    return _ensure_strict_json_schema(schema, path=(), root=schema)


def _ensure_strict_json_schema(
    json_schema: object,
    *,
    path: tuple[str, ...],
    root: dict[str, object],
) -> dict[str, Any]:
    """Enforce strict JSON Schema semantics for LLM structured outputs.

    - additionalProperties: false on all objects
    - All properties marked required (optional fields use union with null)
    - oneOf normalized to anyOf
    - $ref resolution when mixed with other properties
    - Path-tracked error handling
    """
    if not is_dict(json_schema):
        raise SchemaError(f"Expected mapping for schema node; path={'/'.join(path)}")

    # Process $defs and definitions
    defs = json_schema.get("$defs")
    if is_dict(defs):
        for def_name, def_schema in defs.items():
            _ensure_strict_json_schema(def_schema, path=(*path, "$defs", def_name), root=root)

    definitions = json_schema.get("definitions")
    if is_dict(definitions):
        for definition_name, definition_schema in definitions.items():
            _ensure_strict_json_schema(definition_schema, path=(*path, "definitions", definition_name), root=root)

    # Enforce additionalProperties: false on objects
    typ = json_schema.get("type")
    if typ == "object":
        if json_schema.get("additionalProperties") is None:
            json_schema["additionalProperties"] = False
        elif json_schema.get("additionalProperties") not in (False,):
            raise SchemaError(f"Strict schema requires additionalProperties: false; path={'/'.join(path)}")

    # Make all properties required
    properties = json_schema.get("properties")
    if is_dict(properties):
        json_schema["required"] = list(properties.keys())
        json_schema["properties"] = {
            key: _ensure_strict_json_schema(prop_schema, path=(*path, "properties", key), root=root)
            for key, prop_schema in properties.items()
        }

    # Process array items
    items = json_schema.get("items")
    if is_dict(items):
        json_schema["items"] = _ensure_strict_json_schema(items, path=(*path, "items"), root=root)

    # Handle anyOf unions
    any_of = json_schema.get("anyOf")
    if is_list(any_of):
        json_schema["anyOf"] = [
            _ensure_strict_json_schema(variant, path=(*path, "anyOf", str(i)), root=root)
            for i, variant in enumerate(any_of)
        ]

    # Convert oneOf to anyOf
    one_of = json_schema.get("oneOf")
    if is_list(one_of):
        existing_any_of = json_schema.get("anyOf")
        if not isinstance(existing_any_of, list):
            existing_any_of = []
        json_schema["anyOf"] = existing_any_of + [
            _ensure_strict_json_schema(entry, path=(*path, "oneOf", str(i)), root=root)
            for i, entry in enumerate(one_of)
        ]
        json_schema.pop("oneOf")

    # Handle allOf intersections
    all_of = json_schema.get("allOf")
    if is_list(all_of):
        if len(all_of) == 1:
            merged = _ensure_strict_json_schema(all_of[0], path=(*path, "allOf", "0"), root=root)
            json_schema.pop("allOf")
            # Merge while preserving local properties and avoiding $defs duplication
            json_schema.update({k: v for k, v in merged.items() if k != "$defs"})
        else:
            json_schema["allOf"] = [
                _ensure_strict_json_schema(entry, path=(*path, "allOf", str(i)), root=root)
                for i, entry in enumerate(all_of)
            ]

    # Strip None defaults (redundant with nullable types)
    default = json_schema.get("default", NOT_GIVEN)
    if default is None:
        json_schema.pop("default", None)

    # Resolve $ref when mixed with other properties
    ref = json_schema.get("$ref")
    if ref and has_more_than_n_keys(json_schema, 1):
        if not isinstance(ref, str):
            raise SchemaError(f"Received non-string $ref: {ref}")

        resolved = resolve_ref(root=root, ref=ref)
        if not is_dict(resolved):
            raise SchemaError(f"Expected $ref {ref!r} to resolve to mapping; got {type(resolved).__name__}")

        # Local properties override referenced ones
        json_schema.update({**resolved, **json_schema})
        json_schema.pop("$ref")
        # Re-process to ensure strict requirements on inlined schema
        return _ensure_strict_json_schema(json_schema, path=path, root=root)

    return json_schema


def resolve_ref(*, root: dict[str, object], ref: str) -> object:
    """Resolve $ref pointer against schema root.

    Args:
        root: Schema root containing definitions
        ref: JSON Pointer reference (#/...)

    Returns:
        Referenced schema fragment

    Raises:
        SchemaError: If reference cannot be resolved
    """
    if not ref.startswith("#/"):
        raise SchemaError(f"Unexpected $ref format {ref!r}")

    target: Any = root
    for part in ref[2:].split("/"):
        if not isinstance(target, dict) or part not in target:
            raise SchemaError(f"Unable to resolve $ref {ref!r} at {part!r}")
        target = target[part]

    if not is_dict(target):
        raise SchemaError(f"Resolved $ref {ref!r} to non-mapping: {type(target).__name__}")

    return target


def is_basemodel_type(typ: type) -> TypeGuard[type[pydantic.BaseModel]]:
    if not inspect.isclass(typ):
        return False
    return issubclass(typ, pydantic.BaseModel)


def is_dataclass_like_type(typ: type) -> bool:
    """Returns True if the given type likely used `@pydantic.dataclass`"""
    return hasattr(typ, "__pydantic_config__")


def is_dict(obj: object) -> TypeGuard[dict[str, object]]:
    # just pretend that we know there are only `str` keys
    # as that check is not worth the performance cost
    return _is_dict(obj)


def has_more_than_n_keys(obj: dict[str, object], n: int) -> bool:
    i = 0
    for _ in obj.keys():
        i += 1
        if i > n:
            return True
    return False
