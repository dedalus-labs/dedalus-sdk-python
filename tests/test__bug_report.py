# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for SDK bug report URL generation."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx

from dedalus_labs._exceptions import APIError, BadRequestError
from dedalus_labs.lib._bug_report import generate_bug_report_url, get_bug_report_url_from_error


# --- generate_bug_report_url ---


def test_minimal_parameters():
    url = generate_bug_report_url()
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    assert parsed.netloc == "github.com"
    assert parsed.path == "/dedalus-labs/dedalus-sdk-python/issues/new"
    assert params["template"] == ["bug-report.yml"]
    assert params["component"] == ["Python SDK"]
    assert "python_version" in params
    assert "platform" in params


def test_all_parameters():
    url = generate_bug_report_url(
        version="0.0.1",
        error_type="APIError",
        error_message="Connection timeout",
        environment="dev",
        request_id="req-123",
        endpoint="/v1/chat/completions",
        method="POST",
    )
    params = parse_qs(urlparse(url).query)

    assert params["version"] == ["0.0.1"]
    assert params["error_type"] == ["APIError"]
    assert params["actual"] == ["Connection timeout"]
    assert params["environment"] == ["dev"]
    assert params["notes"][0] == "Request ID: req-123\nEndpoint: POST /v1/chat/completions"


def test_request_id_in_notes():
    params = parse_qs(urlparse(generate_bug_report_url(request_id="req-abc-123")).query)
    assert "Request ID: req-abc-123" in params["notes"][0]


def test_custom_template():
    params = parse_qs(urlparse(generate_bug_report_url(template="custom.yml")).query)
    assert params["template"] == ["custom.yml"]


# --- get_bug_report_url_from_error ---


def test_basic_api_error():
    request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
    error = APIError("Request failed", request, body=None)
    params = parse_qs(urlparse(get_bug_report_url_from_error(error)).query)

    assert params["error_type"] == ["APIError"]
    assert params["actual"] == ["Request failed"]
    assert "version" in params


def test_status_error_with_code():
    request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
    response = httpx.Response(400, request=request)
    error = BadRequestError("Invalid request", response=response, body=None)
    params = parse_qs(urlparse(get_bug_report_url_from_error(error)).query)

    assert params["error_type"] == ["BadRequestError"]
    assert "[400]" in params["actual"][0]
    assert "Invalid request" in params["actual"][0]


def test_error_with_request_id():
    request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
    error = APIError("Test error", request, body=None)
    params = parse_qs(urlparse(get_bug_report_url_from_error(error, request_id="req-456")).query)
    assert "Request ID: req-456" in params["notes"][0]


def test_includes_sdk_version():
    request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
    error = APIError("Test error", request, body=None)
    params = parse_qs(urlparse(get_bug_report_url_from_error(error)).query)
    assert len(params["version"][0]) > 0


# --- Platform info ---


def test_platform_info_format():
    params = parse_qs(urlparse(generate_bug_report_url()).query)
    parts = params["platform"][0].split()
    assert len(parts) >= 2


def test_python_version_format():
    params = parse_qs(urlparse(generate_bug_report_url()).query)
    python_version = params["python_version"][0]
    assert python_version.startswith("Python ")
    assert python_version.replace("Python ", "")[0].isdigit()


# --- URL encoding ---


def test_special_chars_encoded():
    url = generate_bug_report_url(
        error_message="Error @ 127.0.0.1:8080 #fail",
        request_id="req/test#123",
    )
    query_string = url.split("?")[1]
    assert "@" not in query_string
    assert "#" not in query_string

    params = parse_qs(urlparse(url).query)
    assert "@" in params["actual"][0]
    assert "#" in params["notes"][0]


def test_unicode_handling():
    url = generate_bug_report_url(error_message="Error: 数据库连接失败")
    params = parse_qs(urlparse(url).query)
    assert "数据库连接失败" in params["actual"][0]
