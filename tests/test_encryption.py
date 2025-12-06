# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for credential encryption."""

from __future__ import annotations

import json
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest

# Skip all tests if cryptography is not installed
pytest.importorskip("cryptography")

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from dedalus_labs.lib.runner.encryption import (
    jwk_to_public_key,
    encrypt_credentials,
    prepare_connection_payload,
    _base64url_encode,
    _base64url_decode,
)


# --- Test fixtures ---


@pytest.fixture
def rsa_keypair() -> tuple[Any, Any]:
    """Generate RSA keypair for testing."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # Smaller for faster tests
        backend=default_backend(),
    )
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture
def rsa_jwk(rsa_keypair: tuple[Any, Any]) -> Dict[str, Any]:
    """Create JWK from keypair."""
    _, public_key = rsa_keypair
    numbers = public_key.public_numbers()

    # Convert to base64url
    n_bytes = numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
    e_bytes = numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")

    return {
        "kty": "RSA",
        "use": "enc",
        "kid": "test-key-1",
        "n": _base64url_encode(n_bytes),
        "e": _base64url_encode(e_bytes),
    }


# --- Tests ---


class TestBase64url:
    """Test base64url encoding/decoding."""

    def test_roundtrip(self) -> None:
        """Encode then decode returns original."""
        data = b"Hello, World!"
        encoded = _base64url_encode(data)
        decoded = _base64url_decode(encoded)
        assert decoded == data

    def test_no_padding(self) -> None:
        """Encoded string has no padding."""
        data = b"test"
        encoded = _base64url_encode(data)
        assert "=" not in encoded

    def test_url_safe(self) -> None:
        """Uses URL-safe characters."""
        data = b"\xff\xfe\xfd"  # Bytes that would produce + and / in standard base64
        encoded = _base64url_encode(data)
        assert "+" not in encoded
        assert "/" not in encoded


class TestJwkToPublicKey:
    """Test JWK to public key conversion."""

    def test_valid_jwk(
        self, rsa_jwk: Dict[str, Any], rsa_keypair: tuple[Any, Any]
    ) -> None:
        """Convert valid JWK to public key."""
        _, expected_public = rsa_keypair

        public_key = jwk_to_public_key(rsa_jwk)

        # Verify it's the same key by comparing public numbers
        assert public_key.public_numbers().n == expected_public.public_numbers().n
        assert public_key.public_numbers().e == expected_public.public_numbers().e

    def test_wrong_kty_raises(self) -> None:
        """Raise on non-RSA key type."""
        jwk = {"kty": "EC", "n": "xxx", "e": "xxx"}

        with pytest.raises(ValueError, match="Expected RSA key"):
            jwk_to_public_key(jwk)

    def test_missing_n_raises(self, rsa_jwk: Dict[str, Any]) -> None:
        """Raise on missing n parameter."""
        del rsa_jwk["n"]

        with pytest.raises(KeyError):
            jwk_to_public_key(rsa_jwk)


class TestEncryptCredentials:
    """Test credential encryption."""

    def test_encrypt_basic(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Encrypt and verify structure."""
        _, public_key = rsa_keypair
        credentials = {"token": "ghp_xxx123"}

        ciphertext = encrypt_credentials(public_key, credentials)

        # Should be base64url string
        assert isinstance(ciphertext, str)
        assert "=" not in ciphertext  # No padding

        # Should be decodable
        ciphertext_bytes = _base64url_decode(ciphertext)
        assert len(ciphertext_bytes) > 0

    def test_encrypt_decrypt_roundtrip(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Encrypted credentials can be decrypted with private key."""
        private_key, public_key = rsa_keypair
        credentials = {"api_key": "sk_test_123", "org_id": "org_456"}

        ciphertext = encrypt_credentials(public_key, credentials)

        # Decrypt
        ciphertext_bytes = _base64url_decode(ciphertext)
        plaintext_bytes = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Verify
        decrypted = json.loads(plaintext_bytes.decode("utf-8"))
        assert decrypted == credentials

    def test_encrypt_multiple_fields(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Encrypt credentials with multiple fields."""
        private_key, public_key = rsa_keypair
        credentials = {
            "username": "admin",
            "password": "s3cr3t",
            "host": "db.example.com",
            "port": 5432,
        }

        ciphertext = encrypt_credentials(public_key, credentials)
        ciphertext_bytes = _base64url_decode(ciphertext)
        plaintext_bytes = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        decrypted = json.loads(plaintext_bytes.decode("utf-8"))
        assert decrypted == credentials

    def test_different_encryptions_differ(self, rsa_keypair: tuple[Any, Any]) -> None:
        """OAEP is randomized - same plaintext produces different ciphertext."""
        _, public_key = rsa_keypair
        credentials = {"token": "same_value"}

        ct1 = encrypt_credentials(public_key, credentials)
        ct2 = encrypt_credentials(public_key, credentials)

        # Ciphertexts should differ due to OAEP randomization
        assert ct1 != ct2


class TestPrepareConnectionPayload:
    """Test complete payload preparation."""

    def test_basic_payload(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Prepare payload from connection and secret."""
        private_key, public_key = rsa_keypair

        # Mock connection
        connection = MagicMock()
        connection.name = "github"
        connection.base_url = "https://api.github.com"
        connection.timeout_ms = 30000

        # Mock secret
        secret = MagicMock()
        secret.values_for_encryption.return_value = {"token": "ghp_xxx"}

        payload = prepare_connection_payload(connection, secret, public_key)

        assert payload["name"] == "github"
        assert payload["base_url"] == "https://api.github.com"
        assert payload["timeout_ms"] == 30000
        assert "encrypted_credentials" in payload
        assert isinstance(payload["encrypted_credentials"], str)

        # Verify decryption
        ciphertext_bytes = _base64url_decode(payload["encrypted_credentials"])
        plaintext_bytes = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        decrypted = json.loads(plaintext_bytes.decode("utf-8"))
        assert decrypted == {"token": "ghp_xxx"}

    def test_with_dict_inputs(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Works with dict inputs too."""
        _, public_key = rsa_keypair

        connection = {"name": "api", "base_url": "https://api.example.com"}
        # Secret dict with 'values' key works with get_secret_values_for_encryption
        secret = {"connection_name": "api", "values": {"key": "xxx"}}

        payload = prepare_connection_payload(connection, secret, public_key)

        assert payload["name"] == "api"
        assert payload["base_url"] == "https://api.example.com"
        assert "encrypted_credentials" in payload


class TestCrossLanguageCompatibility:
    """Document expected wire format for other language implementations."""

    def test_encryption_format_documentation(
        self, rsa_keypair: tuple[Any, Any]
    ) -> None:
        """Document the exact encryption format."""
        private_key, public_key = rsa_keypair
        credentials = {"token": "test_value"}

        ciphertext = encrypt_credentials(public_key, credentials)

        # Document format for other implementations:
        # 1. Input: JSON object with credentials
        # 2. Serialize: json.dumps with separators=(',', ':') - compact, no spaces
        # 3. Encrypt: RSA-OAEP with SHA-256 for both hash and MGF1
        # 4. Encode: base64url without padding

        # The plaintext that was encrypted:
        expected_plaintext = '{"token":"test_value"}'

        # Verify by decrypting
        ciphertext_bytes = _base64url_decode(ciphertext)
        plaintext_bytes = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        assert plaintext_bytes.decode("utf-8") == expected_plaintext


class TestWireSecurityInvariants:
    """Verify security invariants for wire format."""

    def test_plaintext_not_in_payload(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Plaintext credentials must NOT appear anywhere in the wire payload."""
        _, public_key = rsa_keypair

        # Sensitive credential values
        secret_token = "ghp_super_secret_github_token_12345"
        secret_password = "my_database_password_xyz"

        connection = MagicMock()
        connection.name = "github"
        connection.base_url = "https://api.github.com"
        connection.timeout_ms = 30000

        secret = MagicMock()
        secret.values_for_encryption.return_value = {
            "token": secret_token,
            "password": secret_password,
        }

        payload = prepare_connection_payload(connection, secret, public_key)

        # Convert entire payload to string for searching
        payload_str = json.dumps(payload)

        # Plaintext secrets must NOT appear in the payload
        assert secret_token not in payload_str
        assert secret_password not in payload_str
        assert "ghp_" not in payload_str  # Not even prefix

        # But encrypted_credentials must be present
        assert "encrypted_credentials" in payload
        assert len(payload["encrypted_credentials"]) > 100  # Ciphertext is long

    def test_payload_structure_for_api(self, rsa_keypair: tuple[Any, Any]) -> None:
        """Verify payload has correct structure for POST /connections."""
        _, public_key = rsa_keypair

        connection = MagicMock()
        connection.name = "dedalus"
        connection.base_url = "https://api.dedalus.ai"
        connection.timeout_ms = 60000

        secret = MagicMock()
        secret.values_for_encryption.return_value = {"api_key": "sk_xxx"}

        payload = prepare_connection_payload(connection, secret, public_key)

        # Required fields for POST /connections
        assert payload["name"] == "dedalus"
        assert payload["base_url"] == "https://api.dedalus.ai"
        assert payload["timeout_ms"] == 60000
        assert "encrypted_credentials" in payload

        # No extra fields with sensitive data
        assert "api_key" not in payload
        assert "token" not in payload
        assert "password" not in payload
        assert "secret" not in payload

    def test_ciphertext_not_reversible_without_key(
        self, rsa_keypair: tuple[Any, Any]
    ) -> None:
        """Ciphertext cannot be decrypted without private key."""
        private_key, public_key = rsa_keypair

        # Generate a different keypair (attacker's key)
        attacker_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )

        credentials = {"token": "sensitive_value"}
        ciphertext = encrypt_credentials(public_key, credentials)
        ciphertext_bytes = _base64url_decode(ciphertext)

        # Attacker cannot decrypt with wrong key
        with pytest.raises(Exception):  # Various crypto errors possible
            attacker_key.decrypt(
                ciphertext_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

        # But correct key works
        plaintext = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        assert b"sensitive_value" in plaintext
