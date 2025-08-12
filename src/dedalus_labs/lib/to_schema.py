import inspect
import logging
from typing import Callable, Dict, Any
from pydantic import BaseModel, create_model

logger = logging.getLogger(__name__)


class SchemaProcessingError(Exception):
    """Base exception for schema processing errors during parsing or analysis."""
    pass


def to_schema(func: Callable) -> Dict[str, Any]:
    """Convert a Python function's signature to an OpenAPI-compatible JSON schema using Pydantic."""
    try:
        sig = inspect.signature(func)
        fields: Dict[str, Any] = {}

        for name, param in sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                msg = (
                    f"Unsupported parameter kind '{param.kind}' for parameter '*{name}' in function '{func.__name__}'. "
                    f"VAR_POSITIONAL (*args) parameters are not supported."
                )
                logger.error(msg)
                raise SchemaProcessingError(msg)
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                msg = (
                    f"Unsupported parameter kind '{param.kind}' for parameter '**{name}' in function '{func.__name__}'. "
                    f"VAR_KEYWORD (**kwargs) parameters are not supported."
                )
                logger.error(msg)
                raise SchemaProcessingError(msg)

            annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
            default = param.default if param.default != inspect.Parameter.empty else ...
            fields[name] = (annotation, default)

        model_name = f"{func.__name__.capitalize()}InputModel"
        DynamicModel = create_model(model_name, **fields)
        schema = DynamicModel.model_json_schema(ref_template="{model}")

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": (inspect.getdoc(func) or "").strip(),
                "parameters": {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", []),
                },
            },
        }

    except Exception as err:
        msg = f"Error generating schema for function '{func.__name__}': {err}"
        logger.error(msg, exc_info=True)
        raise SchemaProcessingError(msg) from err