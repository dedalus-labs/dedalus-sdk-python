# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Client-side credential encryption using hybrid RSA-OAEP + AES-GCM.

Credentials are encrypted locally before transmission. The envelope format:
  [version:1][wrapped_key:256][nonce:12][ciphertext+tag:variable]

Requires: uv pip install 'dedalus-labs[auth]'
"""

from __future__ import annotations

import base64
import json
import os
from typing import Any

try:
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.backends import default_backend

    _CRYPTO_AVAILABLE = True
except ImportError:
    _CRYPTO_AVAILABLE = False

# Envelope constants
_ENVELOPE_VERSION = 0x01
_NONCE_LEN = 12
_AES_KEY_LEN = 32


def _require_crypto() -> None:
    """Raise if cryptography is not installed."""
    if not _CRYPTO_AVAILABLE:
        raise ImportError(
            "cryptography is required for credential encryption. Install with: uv pip install 'dedalus-labs[auth]'"
        )


def _b64url_encode(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    """Base64url decode with padding restoration."""
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


def jwk_to_public_key(jwk: dict[str, Any], min_key_size: int = 2048) -> Any:
    """Convert a JWK to an RSA public key.

    Args:
        jwk: JWK dict with kty="RSA", n, and e fields.
        min_key_size: Minimum key size in bits (default 2048).

    Returns:
        RSA public key object.

    Raises:
        ImportError: If cryptography is not installed.
        ValueError: If JWK is invalid or key too small.
    """
    _require_crypto()

    if jwk.get("kty") != "RSA":
        raise ValueError(f"expected RSA key type, got: {jwk.get('kty')}")

    try:
        n_bytes = _b64url_decode(jwk["n"])
        e_bytes = _b64url_decode(jwk["e"])
    except KeyError as e:
        raise ValueError(f"missing required JWK field: {e}") from e

    n = int.from_bytes(n_bytes, "big")
    e = int.from_bytes(e_bytes, "big")

    if n.bit_length() < min_key_size:
        raise ValueError(f"key size {n.bit_length()} bits below minimum {min_key_size}")

    return RSAPublicNumbers(e, n).public_key(default_backend())


def encrypt_credentials(public_key: Any, credentials: dict[str, Any]) -> str:
    """Encrypt credentials using hybrid RSA-OAEP + AES-GCM.

    Args:
        public_key: RSA public key from jwk_to_public_key().
        credentials: Credential values to encrypt.

    Returns:
        Base64url-encoded encrypted envelope.

    Raises:
        ImportError: If cryptography is not installed.
    """
    _require_crypto()

    plaintext = json.dumps(credentials, separators=(",", ":")).encode("utf-8")

    # Generate ephemeral AES key and nonce
    aes_key = os.urandom(_AES_KEY_LEN)
    nonce = os.urandom(_NONCE_LEN)

    # Wrap AES key with RSA-OAEP
    wrapped_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Encrypt with AES-GCM
    ciphertext = AESGCM(aes_key).encrypt(nonce, plaintext, None)

    # Assemble envelope: version || wrapped_key || nonce || ciphertext+tag
    envelope = bytes([_ENVELOPE_VERSION]) + wrapped_key + nonce + ciphertext
    return _b64url_encode(envelope)


async def fetch_encryption_key(http_client: Any, as_url: str, key_id: str | None = None) -> Any:
    """Fetch encryption public key from authorization server JWKS.

    Args:
        http_client: httpx.AsyncClient instance.
        as_url: Authorization server base URL.
        key_id: Optional specific key ID.

    Returns:
        RSA public key object.

    Raises:
        ValueError: If no suitable encryption key found.
        RuntimeError: On HTTP errors.
    """
    url = f"{as_url.rstrip('/')}/.well-known/jwks.json"
    response = await http_client.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"failed to fetch JWKS from {url}: {response.status_code}")

    for key in response.json().get("keys", []):
        if key.get("kty") != "RSA" or key.get("use") != "enc":
            continue
        if key_id and key.get("kid") != key_id:
            continue
        return jwk_to_public_key(key)

    raise ValueError(f"no RSA encryption key found at {url}")


def fetch_encryption_key_sync(http_client: Any, as_url: str, key_id: str | None = None) -> Any:
    """Synchronous version of fetch_encryption_key."""
    url = f"{as_url.rstrip('/')}/.well-known/jwks.json"
    response = http_client.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"failed to fetch JWKS from {url}: {response.status_code}")

    for key in response.json().get("keys", []):
        if key.get("kty") != "RSA" or key.get("use") != "enc":
            continue
        if key_id and key.get("kid") != key_id:
            continue
        return jwk_to_public_key(key)

    raise ValueError(f"no RSA encryption key found at {url}")


__all__ = [
    "jwk_to_public_key",
    "encrypt_credentials",
    "fetch_encryption_key",
    "fetch_encryption_key_sync",
]
