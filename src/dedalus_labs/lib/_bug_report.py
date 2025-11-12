# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Bug report URL generation for SDK users."""

from __future__ import annotations

import platform
import sys
from typing import TYPE_CHECKING
from urllib.parse import urlencode

if TYPE_CHECKING:
    from dedalus_labs._exceptions import APIError


__all__ = ["generate_bug_report_url", "get_bug_report_url_from_error"]


BASE_ISSUE_URL = "https://github.com/dedalus-labs/dedalus-sdk-python/issues/new"


def generate_bug_report_url(
    *,
    version: str | None = None,
    error_type: str | None = None,
    error_message: str | None = None,
    endpoint: str | None = None,
    method: str | None = None,
    request_id: str | None = None,
    environment: str | None = None,
    template: str = "bug-report.yml",
) -> str:
    """
    Generate pre-filled GitHub issue URL for SDK bug reports.

    Auto-populates system context (Python version, platform) and allows
    caller to provide error details. URL parameters match field IDs in
    .github/ISSUE_TEMPLATE/bug-report.yml.

    Args:
        version: SDK version string
        error_type: Exception class name
        error_message: Brief error description
        endpoint: API endpoint path (e.g., /v1/chat/completions)
        method: HTTP method (GET, POST, etc.)
        request_id: Request ID from API response headers for log correlation
        environment: dev/staging/prod
        template: GitHub issue template filename

    Returns:
        GitHub issue URL with pre-filled fields

    Example:
        >>> url = generate_bug_report_url(
        ...     version="0.0.1",
        ...     error_type="APIError",
        ...     error_message="Connection timeout",
        ...     endpoint="/v1/chat/completions",
        ...     method="POST",
        ... )
    """
    params = {"template": template, "component": "Python SDK"}

    if version:
        params["version"] = version
    if error_type:
        params["error_type"] = error_type

    # Auto-populate system info
    params["python_version"] = f"Python {sys.version.split()[0]}"
    params["platform"] = _get_platform_info()

    if environment:
        params["environment"] = environment

    # Construct notes field with request context
    notes_parts = []
    if request_id:
        notes_parts.append(f"Request ID: {request_id}")
    if endpoint:
        notes_parts.append(f"Endpoint: {method or 'POST'} {endpoint}")
    if notes_parts:
        params["notes"] = "\n".join(notes_parts)

    # Error message goes in actual field
    if error_message:
        params["actual"] = error_message

    return f"{BASE_ISSUE_URL}?{urlencode(params)}"


def get_bug_report_url_from_error(error: APIError, *, request_id: str | None = None) -> str:
    """
    Generate bug report URL from SDK exception instance.

    Extracts error context automatically from the exception object,
    including error type, message, request details (endpoint, method),
    and optionally request ID from response headers.

    Args:
        error: SDK exception instance (APIError or subclass)
        request_id: Optional request ID override (auto-extracted from response if available)

    Returns:
        GitHub issue URL with error context pre-filled

    Example:
        >>> try:
        ...     client.chat.completions.create(...)
        ... except dedalus_labs.APIError as e:
        ...     url = get_bug_report_url_from_error(e)
        ...     print(f"Report bug: {url}")
    """
    from dedalus_labs import __version__

    error_type = type(error).__name__
    error_message = str(error)

    # Extract status code if available
    if hasattr(error, "status_code"):
        error_message = f"[{error.status_code}] {error_message}"

    # Extract request details
    endpoint = None
    method = None
    if hasattr(error, "request"):
        endpoint = str(error.request.url.path) if error.request.url else None
        method = error.request.method

    # Extract request_id from response headers if not provided
    if request_id is None and hasattr(error, "response"):
        request_id = error.response.headers.get("x-request-id")

    return generate_bug_report_url(
        version=__version__,
        error_type=error_type,
        error_message=error_message,
        endpoint=endpoint,
        method=method,
        request_id=request_id,
    )


def _get_platform_info() -> str:
    """Format platform info: 'Darwin 24.6.0 arm64' or 'Linux 5.15.0 x86_64'."""
    return f"{platform.system()} {platform.release()} {platform.machine()}"
