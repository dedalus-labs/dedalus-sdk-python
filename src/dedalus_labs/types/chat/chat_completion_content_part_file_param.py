# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ChatCompletionContentPartFileParam", "File"]


class File(TypedDict, total=False):
    """Schema for File.

    Fields:
    - filename (optional): str
    - file_data (optional): str
    - file_id (optional): str
    """

    file_data: str
    """
    The base64 encoded file data, used when passing the file to the model as a
    string.
    """

    file_id: str
    """The ID of an uploaded file to use as input."""

    filename: str
    """The name of the file, used when passing the file to the model as a string."""


class ChatCompletionContentPartFileParam(TypedDict, total=False):
    """
    Learn about [file inputs](https://platform.openai.com/docs/guides/text) for text generation.

    Fields:
    - type (required): Literal["file"]
    - file (required): File
    """

    file: Required[File]
    """Schema for File.

    Fields:

    - filename (optional): str
    - file_data (optional): str
    - file_id (optional): str
    """

    type: Required[Literal["file"]]
    """The type of the content part. Always `file`."""
