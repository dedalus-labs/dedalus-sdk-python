from __future__ import annotations

import io
from typing import Any, Iterable
from typing_extensions import TypeAlias

import rich
import pytest
import pydantic

ReprArgs: TypeAlias = "Iterable[tuple[str | None, Any]]"


def rich_print_str(obj: object) -> str:
    """Pretty print an object to a string using rich."""
    buf = io.StringIO()
    console = rich.console.Console(file=buf, force_terminal=True, width=120)
    console.print(obj)
    return buf.getvalue().rstrip("\n")


def print_obj(obj: object, monkeypatch: pytest.MonkeyPatch) -> str:
    """Pretty print an object to a string with deterministic Pydantic field ordering."""
    original_repr = pydantic.BaseModel.__repr_args__

    def __repr_args__(self: pydantic.BaseModel) -> ReprArgs:
        return sorted(original_repr(self), key=lambda arg: arg[0] or "")

    with monkeypatch.context() as m:
        m.setattr(pydantic.BaseModel, "__repr_args__", __repr_args__)
        return rich_print_str(obj)
