# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from . import chat, shared, response
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
    VoiceIDsOrCustomVoice as VoiceIDsOrCustomVoice,
    ResponseFormatJSONObject as ResponseFormatJSONObject,
    ResponseFormatJSONSchema as ResponseFormatJSONSchema,
)
from .ocr_page import OCRPage as OCRPage
from .response import Response as Response
from .ocr_response import OCRResponse as OCRResponse
from .images_response import ImagesResponse as ImagesResponse
from .image_edit_params import ImageEditParams as ImageEditParams
from .ocr_document_param import OCRDocumentParam as OCRDocumentParam
from .ocr_process_params import OCRProcessParams as OCRProcessParams
from .list_models_response import ListModelsResponse as ListModelsResponse
from .image_generate_params import ImageGenerateParams as ImageGenerateParams
from .response_create_params import ResponseCreateParams as ResponseCreateParams
from .embedding_create_params import EmbeddingCreateParams as EmbeddingCreateParams
from .create_embedding_response import CreateEmbeddingResponse as CreateEmbeddingResponse
from .image_create_variation_params import ImageCreateVariationParams as ImageCreateVariationParams

# Rebuild cyclical models only after all modules are imported.
# This ensures that, when building the deferred (due to cyclical references) model schema,
# Pydantic can resolve the necessary references.
# See: https://github.com/pydantic/pydantic/issues/11250 for more context.
if _compat.PYDANTIC_V1:
    response.Response.update_forward_refs()  # type: ignore
    chat.chat_completion.ChatCompletion.update_forward_refs()  # type: ignore
    chat.deferred_call_response.DeferredCallResponse.update_forward_refs()  # type: ignore
    shared.dedalus_model.DedalusModel.update_forward_refs()  # type: ignore
    shared.mcp_tool_result.MCPToolResult.update_forward_refs()  # type: ignore
    shared.model_settings.ModelSettings.update_forward_refs()  # type: ignore
else:
    response.Response.model_rebuild(_parent_namespace_depth=0)
    chat.chat_completion.ChatCompletion.model_rebuild(_parent_namespace_depth=0)
    chat.deferred_call_response.DeferredCallResponse.model_rebuild(_parent_namespace_depth=0)
    shared.dedalus_model.DedalusModel.model_rebuild(_parent_namespace_depth=0)
    shared.mcp_tool_result.MCPToolResult.model_rebuild(_parent_namespace_depth=0)
    shared.model_settings.ModelSettings.model_rebuild(_parent_namespace_depth=0)
