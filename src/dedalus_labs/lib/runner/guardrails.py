# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

from __future__ import annotations

from typing import Any, Callable
from dataclasses import dataclass

__all__ = [
    "GuardrailCheckResult",
    "GuardrailFunc",
    "InputGuardrailTriggered",
    "OutputGuardrailTriggered",
    "input_guardrail",
    "output_guardrail",
]


@dataclass
class GuardrailCheckResult:
    tripwire_triggered: bool
    info: Any = None


GuardrailFunc = Callable[[Any], GuardrailCheckResult | bool | None]


class InputGuardrailTriggered(RuntimeError):
    def __init__(self, result: GuardrailCheckResult):
        super().__init__("Input guardrail tripwire triggered")
        self.result = result


class OutputGuardrailTriggered(RuntimeError):
    def __init__(self, result: GuardrailCheckResult):
        super().__init__("Output guardrail tripwire triggered")
        self.result = result


def input_guardrail(func: GuardrailFunc | None = None, *, name: str | None = None) -> GuardrailFunc | Callable[[GuardrailFunc], GuardrailFunc]:
    """Decorator used to mark a callable as an input guardrail.

    Usage mirrors the backend helpers but the callable is expected to accept the
    pre-call conversation payload (list of messages) and return either a
    `GuardrailCheckResult`, a tuple `(triggered, info)`, a boolean, or ``None``.
    """

    def decorator(fn: GuardrailFunc) -> GuardrailFunc:
        fn._guardrail_name = name or getattr(fn, "__name__", "input_guardrail")
        return fn

    if func is not None:
        return decorator(func)
    return decorator


def output_guardrail(func: GuardrailFunc | None = None, *, name: str | None = None) -> GuardrailFunc | Callable[[GuardrailFunc], GuardrailFunc]:
    """Decorator used to mark a callable as an output guardrail.

    The callable receives the final assistant message string.
    """

    def decorator(fn: GuardrailFunc) -> GuardrailFunc:
        fn._guardrail_name = name or getattr(fn, "__name__", "output_guardrail")
        return fn

    if func is not None:
        return decorator(func)
    return decorator
