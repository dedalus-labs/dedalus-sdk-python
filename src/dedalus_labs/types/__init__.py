# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from . import chat, shared
from .. import _compat
from .image import Image as Image
from .model import Model as Model
from .shared import (
    Reasoning as Reasoning,
    Credential as Credential,
    MCPServers as MCPServers,
    ToolChoice as ToolChoice,
    DedalusModel as DedalusModel,
    MCPServerSpec as MCPServerSpec,
    MCPToolResult as MCPToolResult,
    ModelSettings as ModelSettings,
    JSONValueInput as JSONValueInput,
    MCPCredentials as MCPCredentials,
    JSONObjectInput as JSONObjectInput,
    DedalusModelChoice as DedalusModelChoice,
    FunctionDefinition as FunctionDefinition,
    ResponseFormatText as ResponseFormatText,
    ResponseFormatJSONObject as ResponseFormatJSONObject,
    ResponseFormatJSONSchema as ResponseFormatJSONSchema,
)
from .images_response import ImagesResponse as ImagesResponse
from .image_edit_params import ImageEditParams as ImageEditParams
from .list_models_response import ListModelsResponse as ListModelsResponse
from .image_generate_params import ImageGenerateParams as ImageGenerateParams
from .embedding_create_params import EmbeddingCreateParams as EmbeddingCreateParams
from .create_embedding_response import CreateEmbeddingResponse as CreateEmbeddingResponse
from .image_create_variation_params import ImageCreateVariationParams as ImageCreateVariationParams

# Rebuild cyclical models only after all modules are imported.
# This ensures that, when building the deferred (due to cyclical references) model schema,
# Pydantic can resolve the necessary references.
# See: https://github.com/pydantic/pydantic/issues/11250 for more context.
if _compat.PYDANTIC_V1:
    chat.chat_completion.ChatCompletion.update_forward_refs()  # type: ignore
    shared.dedalus_model.DedalusModel.update_forward_refs()  # type: ignore
    shared.function_definition.FunctionDefinition.update_forward_refs()  # type: ignore
    shared.mcp_tool_result.MCPToolResult.update_forward_refs()  # type: ignore
    shared.model_settings.ModelSettings.update_forward_refs()  # type: ignore
    shared.response_format_json_schema.ResponseFormatJSONSchema.update_forward_refs()  # type: ignore
else:
    chat.chat_completion.ChatCompletion.model_rebuild(_parent_namespace_depth=0)
    shared.dedalus_model.DedalusModel.model_rebuild(_parent_namespace_depth=0)
    shared.function_definition.FunctionDefinition.model_rebuild(_parent_namespace_depth=0)
    shared.mcp_tool_result.MCPToolResult.model_rebuild(_parent_namespace_depth=0)
    shared.model_settings.ModelSettings.model_rebuild(_parent_namespace_depth=0)
    shared.response_format_json_schema.ResponseFormatJSONSchema.model_rebuild(_parent_namespace_depth=0)
