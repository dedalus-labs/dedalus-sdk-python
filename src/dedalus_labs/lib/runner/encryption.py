# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Client-side credential encryption for connection provisioning.

RSA-OAEP-SHA256 encryption of credentials before transmission to the AS.
The server holds the private key; only it can decrypt.

Algorithm: RSA-OAEP with SHA-256 (MGF1 with SHA-256), 3072-bit key recommended
Wire format: base64url-encoded ciphertext

Usage:
    public_key = await fetch_encryption_public_key(http_client, as_url)
    ciphertext = encrypt_credentials(public_key, {"token": "ghp_xxx"})
"""

from __future__ import annotations

import base64
import json
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    pass

# Lazy import cryptography to make it optional
_cryptography_available: Optional[bool] = None


def _check_cryptography() -> bool:
    """Check if cryptography is available."""
    global _cryptography_available
    if _cryptography_available is None:
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa, padding
            from cryptography.hazmat.primitives import hashes

            _cryptography_available = True
        except ImportError:
            _cryptography_available = False
    return _cryptography_available


def _base64url_encode(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def _base64url_decode(s: str) -> bytes:
    """Base64url decode with padding restoration."""
    padding_needed = 4 - len(s) % 4
    if padding_needed != 4:
        s += '=' * padding_needed
    return base64.urlsafe_b64decode(s)


def jwk_to_public_key(jwk: Dict[str, Any], min_key_size: int = 2048) -> Any:
    """Convert JWK to RSA public key object.

    Args:
        jwk: JWK dict with kty="RSA", n, e fields
        min_key_size: Minimum acceptable key size in bits (default: 2048)

    Returns:
        RSA public key object (cryptography.hazmat.primitives.asymmetric.rsa.RSAPublicKey)

    Raises:
        ImportError: If cryptography is not installed
        ValueError: If JWK is invalid or key is too weak

    """
    if not _check_cryptography():
        raise ImportError(
            'cryptography is required for credential encryption. '
            "Install with: pip install 'dedalus_labs[auth]'"
        )

    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
    from cryptography.hazmat.backends import default_backend

    if jwk.get('kty') != 'RSA':
        raise ValueError(f'Expected RSA key, got kty={jwk.get("kty")}')

    n_bytes = _base64url_decode(jwk['n'])
    e_bytes = _base64url_decode(jwk['e'])

    n = int.from_bytes(n_bytes, 'big')
    e = int.from_bytes(e_bytes, 'big')

    # Validate key size before constructing key object
    # n.bit_length() gives actual key size
    key_bits = n.bit_length()
    if key_bits < min_key_size:
        raise ValueError(
            f'RSA key too weak: {key_bits} bits (minimum: {min_key_size}). '
            'This could indicate a malformed or malicious JWKS response.'
        )

    public_numbers = RSAPublicNumbers(e, n)
    return public_numbers.public_key(default_backend())


def encrypt_credentials(public_key: Any, credentials: Dict[str, Any]) -> str:
    """Encrypt credentials with RSA-OAEP-SHA256.

    Args:
        public_key: RSA public key (from jwk_to_public_key)
        credentials: Dict of credential values to encrypt

    Returns:
        Base64url-encoded ciphertext

    Raises:
        ImportError: If cryptography is not installed

    """
    if not _check_cryptography():
        raise ImportError(
            'cryptography is required for credential encryption. '
            "Install with: pip install 'dedalus_labs[auth]'"
        )

    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes

    plaintext = json.dumps(credentials, separators=(',', ':')).encode('utf-8')

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return _base64url_encode(ciphertext)


async def fetch_encryption_public_key(
    http_client: Any,
    as_url: str,
    key_id: Optional[str] = None,
) -> Any:
    """Fetch the encryption public key from the AS JWKS endpoint.

    Looks for an RSA key with use="enc" in the standard JWKS endpoint.

    Args:
        http_client: httpx.AsyncClient instance
        as_url: Authorization Server base URL
        key_id: Optional specific key ID (uses first matching key if None)

    Returns:
        RSA public key object

    Raises:
        ValueError: If no suitable encryption key found
        httpx.HTTPError: On network errors

    """
    url = f'{as_url.rstrip("/")}/.well-known/jwks.json'
    response = await http_client.get(url)
    response.raise_for_status()

    jwks = response.json()
    keys = jwks.get('keys', [])

    if not keys:
        raise ValueError(f'No keys found at {url}')

    # Find RSA key with use="enc"
    for key in keys:
        if key.get('kty') != 'RSA':
            continue
        if key.get('use') != 'enc':
            continue
        if key_id and key.get('kid') != key_id:
            continue
        return jwk_to_public_key(key)

    raise ValueError(
        f'No RSA encryption key (use="enc") found at {url}. '
        'Ensure AS_ENCRYPTION_KEY is configured on the Authorization Server.'
    )


def fetch_encryption_public_key_sync(
    http_client: Any,
    as_url: str,
    key_id: Optional[str] = None,
) -> Any:
    """Synchronous version of fetch_encryption_public_key."""
    url = f'{as_url.rstrip("/")}/.well-known/jwks.json'
    response = http_client.get(url)
    response.raise_for_status()

    jwks = response.json()
    keys = jwks.get('keys', [])

    if not keys:
        raise ValueError(f'No keys found at {url}')

    for key in keys:
        if key.get('kty') != 'RSA':
            continue
        if key.get('use') != 'enc':
            continue
        if key_id and key.get('kid') != key_id:
            continue
        return jwk_to_public_key(key)

    raise ValueError(
        f'No RSA encryption key (use="enc") found at {url}. '
        'Ensure AS_ENCRYPTION_KEY is configured on the Authorization Server.'
    )


def prepare_connection_payload(
    connection: Any,
    credential: Any,
    public_key: Any,
) -> Dict[str, Any]:
    """Prepare encrypted connection payload for POST /connections.

    This is the main entry point for connection provisioning. It:
    1. Extracts credential values from Credential
    2. Encrypts them with the encryption public key
    3. Returns the complete payload for the API

    Args:
        connection: Connection object with name, base_url, timeout_ms
        credential: Credential object with values_for_encryption()
        public_key: RSA public key from fetch_encryption_public_key

    Returns:
        Dict ready for POST /connections

    """
    from .mcp_wire import get_credential_values_for_encryption

    # Get plaintext credentials
    cred_values = get_credential_values_for_encryption(credential)

    # Encrypt
    encrypted = encrypt_credentials(public_key, cred_values)

    # Build payload
    return {
        'name': getattr(connection, 'name', connection.get('name', 'unknown')),
        'base_url': getattr(connection, 'base_url', connection.get('base_url')),
        'timeout_ms': getattr(
            connection, 'timeout_ms', connection.get('timeout_ms', 30000)
        ),
        'encrypted_credentials': encrypted,
    }


__all__ = [
    'jwk_to_public_key',
    'encrypt_credentials',
    'fetch_encryption_public_key',
    'fetch_encryption_public_key_sync',
    'prepare_connection_payload',
]
