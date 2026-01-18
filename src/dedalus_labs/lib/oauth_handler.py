"""OAuth browser flow handler for MCP servers.

When the Product API returns 401 with error=oauth_required, this module:
1. Opens the connect_url in the user's browser
2. Polls the Admin API to check when OAuth is complete
3. Signals the SDK to retry the request
"""

from __future__ import annotations

import time
import webbrowser
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx


def is_oauth_required(body: Any) -> bool:
    """Check if an error response indicates OAuth is required."""
    if not isinstance(body, dict):
        return False
    return body.get("error") == "oauth_required"


def get_connect_url(body: Any) -> str | None:
    """Extract connect_url from an oauth_required error response."""
    if not isinstance(body, dict):
        return None
    return body.get("connect_url")


def get_poll_url(body: Any) -> str | None:
    """Extract poll_url from an oauth_required error response."""
    if not isinstance(body, dict):
        return None
    return body.get("poll_url")


def get_server_id(body: Any) -> str | None:
    """Extract server_id from an oauth_required error response."""
    if not isinstance(body, dict):
        return None
    return body.get("server_id")


def _build_poll_url_from_connect(connect_url: str) -> str | None:
    """Build a poll URL from the connect URL.

    Extracts the server ID from connect_url and builds a poll URL.
    connect_url format: https://admin.dedaluslabs.ai/v1/oauth/connect?server=XXX
    poll_url format: https://admin.dedaluslabs.ai/v1/oauth/servers
    """
    parsed = urlparse(connect_url)
    params = parse_qs(parsed.query)

    if "server" not in params:
        return None

    # Build poll URL pointing to /v1/oauth/servers
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    return f"{base_url}/v1/oauth/servers"


def handle_oauth_flow(
    connect_url: str,
    *,
    poll_url: str | None = None,
    server_id: str | None = None,
    auth_headers: dict[str, str] | None = None,
    poll_interval: float = 2.0,
    timeout: float = 120.0,
) -> bool:
    """Handle the OAuth browser flow.

    1. Opens browser to connect_url
    2. Polls poll_url until OAuth completes or timeout
    3. Returns True if OAuth completed, False if timed out

    Args:
        connect_url: URL to open in browser for OAuth
        poll_url: Optional URL to poll for completion
        server_id: Optional server ID to check in poll response
        auth_headers: Optional auth headers to include in poll requests
        poll_interval: Seconds between poll attempts
        timeout: Maximum seconds to wait for OAuth completion

    Returns:
        True if OAuth completed successfully, False if timed out
    """
    # Open browser
    print(f"\n🔐 OAuth required. Opening browser to authenticate...")
    print(f"   If browser doesn't open, visit: {connect_url}\n")
    webbrowser.open(connect_url)

    # Try to build poll URL from connect URL if not provided
    if not poll_url:
        poll_url = _build_poll_url_from_connect(connect_url)

    # Extract server_id from connect_url if not provided
    if not server_id:
        parsed = urlparse(connect_url)
        params = parse_qs(parsed.query)
        if "server" in params:
            server_id = params["server"][0]

    # If no poll URL, we can't detect completion - just wait a bit and hope
    if not poll_url:
        print("   Waiting for authentication... (press Ctrl+C to cancel)")
        time.sleep(10)  # Give user time to complete OAuth
        return True

    # Poll for completion
    start_time = time.time()
    headers = auth_headers or {}

    with httpx.Client(timeout=10.0) as client:
        while time.time() - start_time < timeout:
            try:
                response = client.get(poll_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # Check if connected - handle both direct response and servers list
                    if data.get("connected"):
                        print("   ✓ Authentication complete!\n")
                        return True
                    # Check servers list for specific server_id or deployment_id
                    # (API returns deployment_id in error but server_id in servers list)
                    if "servers" in data and server_id:
                        for server in data["servers"]:
                            matches = (
                                server.get("server_id") == server_id
                                or server.get("deployment_id") == server_id
                            )
                            if matches and server.get("connected"):
                                print("   ✓ Authentication complete!\n")
                                return True
            except Exception:
                pass  # Ignore poll errors

            time.sleep(poll_interval)

    print("   ⚠ Authentication timed out. Please try again.\n")
    return False


async def handle_oauth_flow_async(
    connect_url: str,
    *,
    poll_url: str | None = None,
    server_id: str | None = None,
    auth_headers: dict[str, str] | None = None,
    poll_interval: float = 2.0,
    timeout: float = 120.0,
) -> bool:
    """Async version of handle_oauth_flow.

    Args:
        connect_url: URL to open in browser for OAuth
        poll_url: Optional URL to poll for completion
        server_id: Optional server ID to check in poll response
        auth_headers: Optional auth headers to include in poll requests
        poll_interval: Seconds between poll attempts
        timeout: Maximum seconds to wait for OAuth completion

    Returns:
        True if OAuth completed successfully, False if timed out
    """
    import asyncio

    # Open browser
    print(f"\n🔐 OAuth required. Opening browser to authenticate...")
    print(f"   If browser doesn't open, visit: {connect_url}\n")
    webbrowser.open(connect_url)

    # Try to build poll URL from connect URL if not provided
    if not poll_url:
        poll_url = _build_poll_url_from_connect(connect_url)

    # Extract server_id from connect_url if not provided
    if not server_id:
        parsed = urlparse(connect_url)
        params = parse_qs(parsed.query)
        if "server" in params:
            server_id = params["server"][0]

    # If no poll URL, we can't detect completion - just wait a bit and hope
    if not poll_url:
        print("   Waiting for authentication... (press Ctrl+C to cancel)")
        await asyncio.sleep(10)
        return True

    # Poll for completion
    start_time = time.time()
    headers = auth_headers or {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        while time.time() - start_time < timeout:
            try:
                response = await client.get(poll_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    # Check if connected - handle both direct response and servers list
                    if data.get("connected"):
                        print("   ✓ Authentication complete!\n")
                        return True
                    # Check servers list for specific server_id or deployment_id
                    # (API returns deployment_id in error but server_id in servers list)
                    if "servers" in data and server_id:
                        for server in data["servers"]:
                            matches = (
                                server.get("server_id") == server_id
                                or server.get("deployment_id") == server_id
                            )
                            if matches and server.get("connected"):
                                print("   ✓ Authentication complete!\n")
                                return True
            except Exception:
                pass  # Ignore poll errors

            await asyncio.sleep(poll_interval)

    print("   ⚠ Authentication timed out. Please try again.\n")
    return False
