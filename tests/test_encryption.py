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


# Envelope v1 constants (must match encryption.py)
_ENVELOPE_VERSION = 0x01
_NONCE_LEN = 12
_TAG_LEN = 16


def _b64url_encode(data: bytes) -> str:
    """Base64url encode without padding (test helper)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    """Base64url decode with padding restoration (test helper)."""
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)


@pytest.fixture
def rsa_keypair() -> tuple[Any, Any]:
    """Generate RSA keypair for testing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


@pytest.fixture
def rsa_keypair_3072() -> tuple[Any, Any]:
    """Generate 3072-bit RSA keypair (production size)."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=3072,
        backend=default_backend(),
    )
    return private_key, private_key.public_key()


@pytest.fixture
def rsa_jwk(rsa_keypair: tuple[Any, Any]) -> dict[str, Any]:
    """Create JWK from keypair."""
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


def decrypt_envelope_v1(private_key: Any, envelope: bytes) -> bytes:
    """Decrypt envelope v1 format (test helper)."""
    key_size = private_key.key_size // 8

    version = envelope[0]
    assert version == _ENVELOPE_VERSION, f"Expected version 0x01, got 0x{version:02x}"

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


class TestJwkToPublicKey:
    """Test JWK to public key conversion."""

    def test_valid_jwk(self, rsa_jwk: dict[str, Any], rsa_keypair: tuple[Any, Any]) -> None:
        """Convert valid JWK to public key."""
        _, expected_public = rsa_keypair
        public_key = jwk_to_public_key(rsa_jwk)

        assert public_key.public_numbers().n == expected_public.public_numbers().n
        assert public_key.public_numbers().e == expected_public.public_numbers().e

    def test_wrong_kty_raises(self) -> None:
        """Raise on non-RSA key type."""
        with pytest.raises(ValueError, match="expected RSA key type"):
            jwk_to_public_key({"kty": "EC", "n": "xxx", "e": "xxx"})

    def test_missing_n_raises(self, rsa_jwk: dict[str, Any]) -> None:
        """Raise on missing n parameter."""
        del rsa_jwk["n"]
        with pytest.raises(ValueError, match="missing required JWK field"):
            jwk_to_public_key(rsa_jwk)

    def test_small_key_rejected(self) -> None:
        """Reject keys smaller than minimum size."""
        small_key = rsa.generate_private_key(65537, 1024, default_backend())
        numbers = small_key.public_key().public_numbers()
        n_bytes = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
        e_bytes = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")

        jwk = {"kty": "RSA", "n": _b64url_encode(n_bytes), "e": _b64url_encode(e_bytes)}

        with pytest.raises(ValueError, match="below minimum"):
            jwk_to_public_key(jwk, min_key_size=2048)


class TestEncryptCredentials:
    """Test credential encryption (envelope v1)."""

    def test_envelope_format(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Encrypt produces valid envelope v1 format."""
        private_key, public_key = rsa_keypair
        credentials = {"token": "ghp_xxx123"}

        ciphertext_b64 = encrypt_credentials(public_key, credentials)
        envelope = _b64url_decode(ciphertext_b64)

        key_size = private_key.key_size // 8
        min_len = 1 + key_size + _NONCE_LEN + _TAG_LEN
        assert len(envelope) >= min_len
        assert envelope[0] == _ENVELOPE_VERSION

    def test_roundtrip(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Encrypted credentials can be decrypted with private key."""
        private_key, public_key = rsa_keypair
        credentials = {"api_key": "sk_test_123", "org_id": "org_456"}

        ciphertext_b64 = encrypt_credentials(public_key, credentials)
        envelope = _b64url_decode(ciphertext_b64)
        plaintext = decrypt_envelope_v1(private_key, envelope)

        assert json.loads(plaintext) == credentials

    def test_large_payload(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Envelope v1 handles payloads larger than RSA limit."""
        private_key, public_key = rsa_keypair
        credentials = {"large_token": "x" * 1000, "another": "y" * 500}

        ciphertext_b64 = encrypt_credentials(public_key, credentials)
        envelope = _b64url_decode(ciphertext_b64)
        plaintext = decrypt_envelope_v1(private_key, envelope)

        assert json.loads(plaintext) == credentials

    def test_randomized(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Same plaintext produces different ciphertext each time."""
        _, public_key = rsa_keypair
        credentials = {"token": "same_value"}

        ct1 = encrypt_credentials(public_key, credentials)
        ct2 = encrypt_credentials(public_key, credentials)

        assert ct1 != ct2

    def test_with_3072_key(self, rsa_keypair_3072: tuple[Any, Any]) -> None:
        """Works with production-size 3072-bit keys."""
        private_key, public_key = rsa_keypair_3072
        credentials = {"token": "production_token"}

        ciphertext_b64 = encrypt_credentials(public_key, credentials)
        envelope = _b64url_decode(ciphertext_b64)
        plaintext = decrypt_envelope_v1(private_key, envelope)

        assert json.loads(plaintext) == credentials


class TestSecurityInvariants:
    """Verify security properties."""

    def test_plaintext_not_in_ciphertext(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Plaintext must not appear in ciphertext."""
        _, public_key = rsa_keypair
        secret = "ghp_super_secret_token_12345"

        ciphertext = encrypt_credentials(public_key, {"token": secret})

        assert secret not in ciphertext
        assert "ghp_" not in ciphertext

    def test_wrong_key_fails(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Decryption fails with wrong private key."""
        _, public_key = rsa_keypair
        attacker_key = rsa.generate_private_key(65537, 2048, default_backend())

        ciphertext_b64 = encrypt_credentials(public_key, {"token": "secret"})
        envelope = _b64url_decode(ciphertext_b64)

        with pytest.raises(Exception):
            decrypt_envelope_v1(attacker_key, envelope)

    def test_tampered_ciphertext_fails(self, rsa_keypair: tuple[Any, Any]) -> None:
        """GCM authentication rejects tampered ciphertext."""
        private_key, public_key = rsa_keypair

        ciphertext_b64 = encrypt_credentials(public_key, {"token": "test"})
        envelope = bytearray(_b64url_decode(ciphertext_b64))

        # Tamper with ciphertext portion
        key_size = private_key.key_size // 8
        envelope[1 + key_size + _NONCE_LEN + 5] ^= 0xFF

        with pytest.raises(Exception):
            decrypt_envelope_v1(private_key, bytes(envelope))

    def test_tampered_wrapped_key_fails(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Tampered wrapped key is rejected."""
        private_key, public_key = rsa_keypair

        ciphertext_b64 = encrypt_credentials(public_key, {"token": "test"})
        envelope = bytearray(_b64url_decode(ciphertext_b64))

        envelope[10] ^= 0xFF

        with pytest.raises(Exception):
            decrypt_envelope_v1(private_key, bytes(envelope))
