# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for credential encryption (envelope v1 format)."""

from __future__ import annotations

import base64
import json
from typing import Any

import pytest

# Skip all tests if cryptography is not installed
pytest.importorskip("cryptography")

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

from dedalus_labs.lib.crypto.encryption import (
    jwk_to_public_key,
    encrypt_credentials,
)


# --- Constants (must match encryption.py) ---

_ENVELOPE_VERSION = 0x01
_NONCE_LEN = 12
_TAG_LEN = 16


# --- Test helpers ---


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


def _decrypt_envelope_v1(private_key: Any, envelope: bytes) -> bytes:
    """Decrypt envelope v1 format."""
    key_size = private_key.key_size // 8
    assert envelope[0] == _ENVELOPE_VERSION
    wrapped_key = envelope[1 : 1 + key_size]
    nonce = envelope[1 + key_size : 1 + key_size + _NONCE_LEN]
    ciphertext_with_tag = envelope[1 + key_size + _NONCE_LEN :]
    aes_key = private_key.decrypt(
        wrapped_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return AESGCM(aes_key).decrypt(nonce, ciphertext_with_tag, None)


# --- Fixtures ---


@pytest.fixture
def rsa_keypair() -> tuple[Any, Any]:
    private_key = rsa.generate_private_key(65537, 2048, default_backend())
    return private_key, private_key.public_key()


@pytest.fixture
def rsa_keypair_3072() -> tuple[Any, Any]:
    private_key = rsa.generate_private_key(65537, 3072, default_backend())
    return private_key, private_key.public_key()


@pytest.fixture
def rsa_jwk(rsa_keypair: tuple[Any, Any]) -> dict[str, Any]:
    _, public_key = rsa_keypair
    numbers = public_key.public_numbers()
    n_bytes = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
    e_bytes = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")
    return {
        "kty": "RSA",
        "use": "enc",
        "kid": "test-key-1",
        "n": _b64url_encode(n_bytes),
        "e": _b64url_encode(e_bytes),
    }


# --- jwk_to_public_key ---


def test_jwk_valid(rsa_jwk: dict[str, Any], rsa_keypair: tuple[Any, Any]):
    _, expected_public = rsa_keypair
    public_key = jwk_to_public_key(rsa_jwk)
    assert public_key.public_numbers().n == expected_public.public_numbers().n
    assert public_key.public_numbers().e == expected_public.public_numbers().e


def test_jwk_wrong_kty_raises():
    with pytest.raises(ValueError, match="expected RSA key type"):
        jwk_to_public_key({"kty": "EC", "n": "xxx", "e": "xxx"})


def test_jwk_missing_n_raises(rsa_jwk: dict[str, Any]):
    del rsa_jwk["n"]
    with pytest.raises(ValueError, match="missing required JWK field"):
        jwk_to_public_key(rsa_jwk)


def test_jwk_small_key_rejected():
    small_key = rsa.generate_private_key(65537, 1024, default_backend())
    numbers = small_key.public_key().public_numbers()
    n_bytes = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
    e_bytes = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")
    jwk = {"kty": "RSA", "n": _b64url_encode(n_bytes), "e": _b64url_encode(e_bytes)}
    with pytest.raises(ValueError, match="below minimum"):
        jwk_to_public_key(jwk, min_key_size=2048)


# --- encrypt_credentials (envelope v1) ---


def test_encrypt_envelope_format(rsa_keypair: tuple[Any, Any]):
    private_key, public_key = rsa_keypair
    ciphertext_b64 = encrypt_credentials(public_key, {"token": "ghp_xxx123"})
    envelope = _b64url_decode(ciphertext_b64)
    key_size = private_key.key_size // 8
    assert len(envelope) >= 1 + key_size + _NONCE_LEN + _TAG_LEN
    assert envelope[0] == _ENVELOPE_VERSION


def test_encrypt_roundtrip(rsa_keypair: tuple[Any, Any]):
    private_key, public_key = rsa_keypair
    credentials = {"api_key": "sk_test_123", "org_id": "org_456"}
    ciphertext_b64 = encrypt_credentials(public_key, credentials)
    plaintext = _decrypt_envelope_v1(private_key, _b64url_decode(ciphertext_b64))
    assert json.loads(plaintext) == credentials


def test_encrypt_large_payload(rsa_keypair: tuple[Any, Any]):
    private_key, public_key = rsa_keypair
    credentials = {"large_token": "x" * 1000, "another": "y" * 500}
    ciphertext_b64 = encrypt_credentials(public_key, credentials)
    plaintext = _decrypt_envelope_v1(private_key, _b64url_decode(ciphertext_b64))
    assert json.loads(plaintext) == credentials


def test_encrypt_randomized(rsa_keypair: tuple[Any, Any]):
    """Same plaintext produces different ciphertext each time."""
    _, public_key = rsa_keypair
    credentials = {"token": "same_value"}
    assert encrypt_credentials(public_key, credentials) != encrypt_credentials(public_key, credentials)


def test_encrypt_with_3072_key(rsa_keypair_3072: tuple[Any, Any]):
    private_key, public_key = rsa_keypair_3072
    credentials = {"token": "production_token"}
    ciphertext_b64 = encrypt_credentials(public_key, credentials)
    plaintext = _decrypt_envelope_v1(private_key, _b64url_decode(ciphertext_b64))
    assert json.loads(plaintext) == credentials


# --- Security invariants ---


def test_plaintext_not_in_ciphertext(rsa_keypair: tuple[Any, Any]):
    _, public_key = rsa_keypair
    secret = "ghp_super_secret_token_12345"
    ciphertext = encrypt_credentials(public_key, {"token": secret})
    assert secret not in ciphertext
    assert "ghp_" not in ciphertext


def test_wrong_key_fails(rsa_keypair: tuple[Any, Any]):
    _, public_key = rsa_keypair
    attacker_key = rsa.generate_private_key(65537, 2048, default_backend())
    ciphertext_b64 = encrypt_credentials(public_key, {"token": "secret"})
    with pytest.raises(Exception):
        _decrypt_envelope_v1(attacker_key, _b64url_decode(ciphertext_b64))


def test_tampered_ciphertext_fails(rsa_keypair: tuple[Any, Any]):
    private_key, public_key = rsa_keypair
    ciphertext_b64 = encrypt_credentials(public_key, {"token": "test"})
    envelope = bytearray(_b64url_decode(ciphertext_b64))
    key_size = private_key.key_size // 8
    envelope[1 + key_size + _NONCE_LEN + 5] ^= 0xFF
    with pytest.raises(Exception):
        _decrypt_envelope_v1(private_key, bytes(envelope))


def test_tampered_wrapped_key_fails(rsa_keypair: tuple[Any, Any]):
    private_key, public_key = rsa_keypair
    ciphertext_b64 = encrypt_credentials(public_key, {"token": "test"})
    envelope = bytearray(_b64url_decode(ciphertext_b64))
    envelope[10] ^= 0xFF
    with pytest.raises(Exception):
        _decrypt_envelope_v1(private_key, bytes(envelope))
