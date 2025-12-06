# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Authentication handlers for the Dedalus SDK.

Provides `DPoPAuth` for sender-constrained tokens (RFC 9449) and `BearerAuth`
for standard OAuth 2.0 bearer tokens.

Usage:
    from dedalus_labs.auth import DPoPAuth, create_dpop_auth

    # Async: fetch token and create auth handler
    auth = await create_dpop_auth(
        token_url="https://auth.dedaluslabs.ai/token",
        client_id="my-client",
    )

    # Pass to client
    client = Dedalus(custom_auth=auth)
"""

from __future__ import annotations

import base64
import hashlib
import time
import uuid
from typing import TYPE_CHECKING, Any, Generator

from typing_extensions import override

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey

import httpx


def _b64url_encode(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _compute_ath(access_token: str) -> str:
    """Compute access token hash (ath claim) per RFC 9449 §6.1."""
    token_hash = hashlib.sha256(access_token.encode()).digest()
    return _b64url_encode(token_hash)


def _compute_jwk_thumbprint(public_key: Any) -> str:
    """Compute JWK thumbprint per RFC 7638."""
    import json

    public_numbers = public_key.public_numbers()
    coord_size = 32  # P-256 = 256 bits = 32 bytes

    x = _b64url_encode(public_numbers.x.to_bytes(coord_size, byteorder='big'))
    y = _b64url_encode(public_numbers.y.to_bytes(coord_size, byteorder='big'))

    # Lexicographically sorted per RFC 7638
    canonical = json.dumps(
        {'crv': 'P-256', 'kty': 'EC', 'x': x, 'y': y},
        separators=(',', ':'),
        sort_keys=True,
    )

    thumbprint = hashlib.sha256(canonical.encode()).digest()
    return _b64url_encode(thumbprint)


def generate_dpop_proof(
    dpop_key: EllipticCurvePrivateKey,
    method: str,
    url: str,
    access_token: str | None = None,
    nonce: str | None = None,
) -> str:
    """Generate a DPoP proof JWT per RFC 9449.

    Args:
        dpop_key: EC private key (P-256/ES256) for signing
        method: HTTP method (e.g., "GET", "POST")
        url: Full HTTP URL (query/fragment stripped per RFC 9449 §4.2)
        access_token: Optional access token to bind via ath claim
        nonce: Optional server-provided nonce

    Returns:
        DPoP proof JWT string
    """
    import jwt
    from urllib.parse import urlparse

    public_key = dpop_key.public_key()
    public_numbers = public_key.public_numbers()

    coord_size = 32
    x = _b64url_encode(public_numbers.x.to_bytes(coord_size, byteorder='big'))
    y = _b64url_encode(public_numbers.y.to_bytes(coord_size, byteorder='big'))

    jwk = {'kty': 'EC', 'crv': 'P-256', 'x': x, 'y': y}
    header = {'typ': 'dpop+jwt', 'alg': 'ES256', 'jwk': jwk}

    # Strip query and fragment from URL, per RFC 9449 §4.2
    parsed = urlparse(url)
    htu = f'{parsed.scheme}://{parsed.netloc}{parsed.path}'
    if not parsed.path:
        htu += '/'

    payload: dict[str, Any] = {
        'jti': str(uuid.uuid4()),
        'htm': method.upper(),
        'htu': htu,
        'iat': int(time.time()),
    }

    if access_token is not None:
        payload['ath'] = _compute_ath(access_token)

    if nonce is not None:
        payload['nonce'] = nonce

    return jwt.encode(payload, dpop_key, algorithm='ES256', headers=header)


class DPoPAuth(httpx.Auth):
    """HTTPX auth handler for DPoP-bound tokens (RFC 9449).

    Generates a fresh DPoP proof for each request, binding the access token
    to the specific HTTP method and URL. Stolen tokens are useless without
    the private key.

    Example:
        from cryptography.hazmat.primitives.asymmetric import ec
        from dedalus_labs.auth import DPoPAuth

        dpop_key = ec.generate_private_key(ec.SECP256R1())
        auth = DPoPAuth(access_token="eyJ...", dpop_key=dpop_key)

        client = Dedalus(custom_auth=auth)
    """

    requires_response_body = False

    def __init__(
        self,
        access_token: str,
        dpop_key: EllipticCurvePrivateKey,
        nonce: str | None = None,
    ) -> None:
        """Initialize DPoP auth handler.

        Args:
            access_token: DPoP-bound OAuth 2.1 access token
            dpop_key: EC private key (P-256) for signing proofs
            nonce: Optional initial nonce from server
        """
        self._access_token = access_token
        self._dpop_key = dpop_key
        self._nonce = nonce

    @property
    def thumbprint(self) -> str:
        """JWK thumbprint of the DPoP key."""
        return _compute_jwk_thumbprint(self._dpop_key.public_key())

    def set_nonce(self, nonce: str | None) -> None:
        """Update the DPoP nonce from DPoP-Nonce response header."""
        self._nonce = nonce

    def set_access_token(self, token: str) -> None:
        """Update the access token after refresh."""
        self._access_token = token

    @override
    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Generate DPoP auth headers for each request."""
        proof = generate_dpop_proof(
            dpop_key=self._dpop_key,
            method=request.method,
            url=str(request.url),
            access_token=self._access_token,
            nonce=self._nonce,
        )

        request.headers['Authorization'] = f'DPoP {self._access_token}'
        request.headers['DPoP'] = proof

        yield request


class BearerAuth(httpx.Auth):
    """Simple bearer token auth handler.

    For servers that don't require DPoP.

    Example:
        auth = BearerAuth(access_token="eyJ...")
        client = Dedalus(custom_auth=auth)
    """

    requires_response_body = False

    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    def set_access_token(self, token: str) -> None:
        """Update the access token after refresh."""
        self._access_token = token

    @override
    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Add Bearer authorization header."""
        request.headers['Authorization'] = f'Bearer {self._access_token}'
        yield request


def create_dpop_keypair() -> 'EllipticCurvePrivateKey':
    """Generate an ephemeral P-256 keypair for DPoP.

    Returns a new EC private key suitable for DPoP proof signing.
    The key is ephemeral (in-memory only) and should not be persisted.

    Returns:
        P-256 EC private key
    """
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.backends import default_backend

    return ec.generate_private_key(ec.SECP256R1(), default_backend())


async def create_dpop_auth(
    api_key: str,
    as_url: str = 'https://as.dedaluslabs.ai',
    http_client: httpx.AsyncClient | None = None,
) -> DPoPAuth:
    """Create a DPoP auth handler with automatic token exchange.

    This is the recommended way to set up DPoP authentication. It:
    1. Generates an ephemeral P-256 keypair
    2. Performs token exchange with the AS (api_key -> DPoP-bound JWT)
    3. Returns a ready-to-use DPoPAuth handler

    Args:
        api_key: Dedalus API key (dsk_xxx)
        as_url: Authorization Server URL
        http_client: Optional httpx client (creates one if not provided)

    Returns:
        Configured DPoPAuth handler

    Example:
        auth = await create_dpop_auth(api_key="dsk_xxx")
        client = Dedalus(custom_auth=auth)
    """
    dpop_key = create_dpop_keypair()

    # Build token exchange request
    token_url = f'{as_url.rstrip("/")}/token'

    # Generate DPoP proof for token endpoint
    proof = generate_dpop_proof(
        dpop_key=dpop_key,
        method='POST',
        url=token_url,
    )

    # Token exchange payload
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
        'subject_token': api_key,
        'subject_token_type': 'urn:dedalus:api-key',
        'scope': 'dispatch',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'DPoP': proof,
    }

    # Make request
    should_close = http_client is None
    if http_client is None:
        http_client = httpx.AsyncClient()

    try:
        response = await http_client.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        token_response = response.json()
        access_token = token_response['access_token']

        # Check for server nonce
        nonce = response.headers.get('DPoP-Nonce')

        return DPoPAuth(
            access_token=access_token,
            dpop_key=dpop_key,
            nonce=nonce,
        )
    finally:
        if should_close:
            await http_client.aclose()


def create_dpop_auth_sync(
    api_key: str,
    as_url: str = 'https://as.dedaluslabs.ai',
    http_client: httpx.Client | None = None,
) -> DPoPAuth:
    """Synchronous version of create_dpop_auth."""
    dpop_key = create_dpop_keypair()

    token_url = f'{as_url.rstrip("/")}/token'

    proof = generate_dpop_proof(
        dpop_key=dpop_key,
        method='POST',
        url=token_url,
    )

    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
        'subject_token': api_key,
        'subject_token_type': 'urn:dedalus:api-key',
        'scope': 'dispatch',
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'DPoP': proof,
    }

    should_close = http_client is None
    if http_client is None:
        http_client = httpx.Client()

    try:
        response = http_client.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        token_response = response.json()
        access_token = token_response['access_token']
        nonce = response.headers.get('DPoP-Nonce')

        return DPoPAuth(
            access_token=access_token,
            dpop_key=dpop_key,
            nonce=nonce,
        )
    finally:
        if should_close:
            http_client.close()


__all__ = [
    'BearerAuth',
    'DPoPAuth',
    'create_dpop_auth',
    'create_dpop_auth_sync',
    'create_dpop_keypair',
    'generate_dpop_proof',
]
