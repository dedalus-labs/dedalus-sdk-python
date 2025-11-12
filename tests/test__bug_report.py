# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for SDK bug report URL generation."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from dedalus_labs._exceptions import APIError, APIStatusError, BadRequestError
from dedalus_labs.lib._bug_report import generate_bug_report_url, get_bug_report_url_from_error


class TestGenerateBugReportUrl:
    """Tests for generate_bug_report_url function."""

    def test_minimal_parameters(self):
        """URL generation with no params includes auto-populated system info."""
        url = generate_bug_report_url()

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert parsed.netloc == "github.com"
        assert parsed.path == "/dedalus-labs/dedalus-sdk-python/issues/new"
        assert params["template"] == ["bug-report.yml"]
        assert params["component"] == ["Python SDK"]
        assert "python_version" in params
        assert "platform" in params

    def test_all_parameters(self):
        """URL generation with all parameters populates fields correctly."""
        url = generate_bug_report_url(
            version="0.0.1",
            error_type="APIError",
            error_message="Connection timeout",
            environment="dev",
            request_id="req-123",
            endpoint="/v1/chat/completions",
            method="POST",
        )

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert params["version"] == ["0.0.1"]
        assert params["error_type"] == ["APIError"]
        assert params["actual"] == ["Connection timeout"]
        assert params["environment"] == ["dev"]
        assert params["notes"][0] == "Request ID: req-123\nEndpoint: POST /v1/chat/completions"

    def test_request_id_in_notes(self):
        """Request ID is included in notes field."""
        url = generate_bug_report_url(request_id="req-abc-123")

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert "notes" in params
        assert "Request ID: req-abc-123" in params["notes"][0]

    def test_custom_template(self):
        """Custom template name is respected."""
        url = generate_bug_report_url(template="custom.yml")

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert params["template"] == ["custom.yml"]


class TestGetBugReportUrlFromError:
    """Tests for get_bug_report_url_from_error function."""

    def test_basic_api_error(self):
        """Generates URL from basic APIError instance."""
        request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
        error = APIError("Request failed", request, body=None)

        url = get_bug_report_url_from_error(error)

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert params["error_type"] == ["APIError"]
        assert params["actual"] == ["Request failed"]
        assert "version" in params

    def test_api_status_error_with_code(self):
        """Status code is included in error message for APIStatusError."""
        request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
        response = httpx.Response(400, request=request)
        error = BadRequestError("Invalid request", response=response, body=None)

        url = get_bug_report_url_from_error(error)

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert params["error_type"] == ["BadRequestError"]
        assert "[400]" in params["actual"][0]
        assert "Invalid request" in params["actual"][0]

    def test_with_request_id(self):
        """Request ID parameter is included when provided."""
        request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
        error = APIError("Test error", request, body=None)

        url = get_bug_report_url_from_error(error, request_id="req-456")

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        assert "notes" in params
        assert "Request ID: req-456" in params["notes"][0]

    def test_includes_sdk_version(self):
        """SDK version is automatically included from __version__."""
        request = httpx.Request("POST", "https://api.dedalus.ai/v1/chat/completions")
        error = APIError("Test error", request, body=None)

        url = get_bug_report_url_from_error(error)

        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        # Should have version parameter populated
        assert "version" in params
        # Should be non-empty
        assert len(params["version"][0]) > 0


class TestPlatformInfo:
    """Tests for platform info collection."""

    def test_platform_info_format(self):
        """Platform info has expected format."""
        url = generate_bug_report_url()

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        platform_info = params["platform"][0]

        # Format: "System Release Machine"
        parts = platform_info.split()
        assert len(parts) >= 2

    def test_python_version_format(self):
        """Python version has expected format."""
        url = generate_bug_report_url()

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        python_version = params["python_version"][0]

        assert python_version.startswith("Python ")
        version_part = python_version.replace("Python ", "")
        assert len(version_part) > 0
        assert version_part[0].isdigit()


class TestUrlEncoding:
    """Tests for URL encoding edge cases."""

    def test_special_chars_encoded(self):
        """Special characters are properly URL-encoded."""
        url = generate_bug_report_url(
            error_message="Error @ 127.0.0.1:8080 #fail",
            request_id="req/test#123",
        )

        # URL query string should not contain raw special chars
        query_string = url.split("?")[1]
        assert "@" not in query_string
        assert "#" not in query_string

        # But decoded params should contain them
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert "@" in params["actual"][0]
        assert "#" in params["notes"][0]

    def test_unicode_handling(self):
        """Unicode characters are properly encoded."""
        url = generate_bug_report_url(error_message="Error: 数据库连接失败")

        # Should not raise and should produce valid URL
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert "数据库连接失败" in params["actual"][0]
