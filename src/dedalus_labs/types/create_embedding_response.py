# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CreateEmbeddingResponse", "Data"]


class Data(BaseModel):
    embedding: Union[List[float], str]
    """The embedding vector (float array or base64 string)"""

    index: int
    """Index of the embedding in the list"""

    object: Optional[Literal["embedding"]] = None
    """Object type, always 'embedding'"""


class CreateEmbeddingResponse(BaseModel):
    data: List[Data]
    """List of embedding objects"""

    model: str
    """The model used for embeddings"""

    usage: Dict[str, int]
    """Usage statistics (prompt_tokens, total_tokens)"""

    object: Optional[Literal["list"]] = None
    """Object type, always 'list'"""
