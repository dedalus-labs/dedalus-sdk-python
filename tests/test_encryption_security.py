# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Security enforcement tests for credential encryption.

These tests are HARD GATES. If any test fails, the build fails.
No gray areas. No TODOs. Secure or broken.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest

pytest.importorskip('cryptography')

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


# --- Invariant: Weak keys must be rejected. -----------------------------------

class TestKeyStrengthEnforcement:
    """RSA keys below 2048 bits MUST be rejected."""

    def test_1024_bit_key_rejected(self) -> None:
        """1024-bit RSA is deprecated. MUST reject."""
        weak_key = rsa.generate_private_key(65537, 1024, default_backend())
        public_numbers = weak_key.public_key().public_numbers()

        n_bytes = public_numbers.n.to_bytes(
            (public_numbers.n.bit_length() + 7) // 8, 'big'
        )
        e_bytes = public_numbers.e.to_bytes(
            (public_numbers.e.bit_length() + 7) // 8, 'big'
        )

        weak_jwk = {
            'kty': 'RSA',
            'n': _base64url_encode(n_bytes),
            'e': _base64url_encode(e_bytes),
        }

        with pytest.raises(ValueError, match='too weak'):
            jwk_to_public_key(weak_jwk)

    def test_2048_bit_key_accepted(self) -> None:
        """2048-bit RSA is minimum acceptable."""
        key = rsa.generate_private_key(65537, 2048, default_backend())
        public_numbers = key.public_key().public_numbers()

        n_bytes = public_numbers.n.to_bytes(
            (public_numbers.n.bit_length() + 7) // 8, 'big'
        )
        e_bytes = public_numbers.e.to_bytes(
            (public_numbers.e.bit_length() + 7) // 8, 'big'
        )

        jwk = {
            'kty': 'RSA',
            'n': _base64url_encode(n_bytes),
            'e': _base64url_encode(e_bytes),
        }

        public_key = jwk_to_public_key(jwk)
        assert public_key.key_size >= 2048

    def test_3072_bit_key_accepted(self) -> None:
        """3072-bit RSA (our production key size) works."""
        key = rsa.generate_private_key(65537, 3072, default_backend())
        public_numbers = key.public_key().public_numbers()

        n_bytes = public_numbers.n.to_bytes(
            (public_numbers.n.bit_length() + 7) // 8, 'big'
        )
        e_bytes = public_numbers.e.to_bytes(
            (public_numbers.e.bit_length() + 7) // 8, 'big'
        )

        jwk = {
            'kty': 'RSA',
            'n': _base64url_encode(n_bytes),
            'e': _base64url_encode(e_bytes),
        }

        public_key = jwk_to_public_key(jwk)
        assert public_key.key_size == 3072

    def test_garbage_base64_rejected(self) -> None:
        """Malformed base64url that decodes to tiny key MUST be rejected."""
        # This garbage decodes to ~96 bits - MUST fail
        malformed_jwk = {
            'kty': 'RSA',
            'n': '!!!not-valid-base64!!!',
            'e': 'AQAB',
        }

        with pytest.raises(ValueError, match='too weak'):
            jwk_to_public_key(malformed_jwk)


# --- Invariant: Invalid JWKs must be rejected. --------------------------------


class TestJWKValidationEnforcement:
    """Invalid JWKs MUST be rejected with clear errors."""

    def test_non_rsa_key_rejected(self) -> None:
        """Only RSA keys accepted for encryption."""
        ec_jwk = {'kty': 'EC', 'crv': 'P-256', 'x': 'xxx', 'y': 'yyy'}

        with pytest.raises(ValueError, match='Expected RSA'):
            jwk_to_public_key(ec_jwk)

    def test_missing_modulus_rejected(self) -> None:
        """JWK without 'n' MUST fail."""
        incomplete_jwk = {'kty': 'RSA', 'e': 'AQAB'}

        with pytest.raises(KeyError):
            jwk_to_public_key(incomplete_jwk)

    def test_missing_exponent_rejected(self) -> None:
        """JWK without 'e' MUST fail."""
        incomplete_jwk = {'kty': 'RSA', 'n': 'abc'}

        with pytest.raises(KeyError):
            jwk_to_public_key(incomplete_jwk)

    def test_zero_modulus_rejected(self) -> None:
        """Zero modulus MUST fail."""
        zero_jwk = {'kty': 'RSA', 'n': 'AA', 'e': 'AQAB'}

        with pytest.raises((ValueError, Exception)):
            jwk_to_public_key(zero_jwk)


# --- Invariant: Plaintext must never leak. ------------------------------------


class TestEncryptionInvariants:
    """Plaintext credentials MUST never appear in wire format."""

    @pytest.fixture
    def keypair(self) -> tuple[Any, Any]:
        private = rsa.generate_private_key(65537, 2048, default_backend())
        return private, private.public_key()

    def test_plaintext_never_in_payload(self, keypair: tuple[Any, Any]) -> None:
        """Plaintext credentials MUST NOT appear anywhere in payload."""
        _, public_key = keypair

        secrets = {
            'token': 'ghp_SUPER_SECRET_TOKEN_12345',
            'password': 'P@ssw0rd_NEVER_LEAK_THIS',
            'api_key': 'sk-live-PRODUCTION_KEY_xyz',
        }

        connection = MagicMock()
        connection.name = 'test'
        connection.base_url = 'https://api.example.com'
        connection.timeout_ms = 30000

        credential = MagicMock()
        credential.values_for_encryption.return_value = secrets

        payload = prepare_connection_payload(connection, credential, public_key)
        payload_str = json.dumps(payload)

        # HARD CHECK: No plaintext in output
        for secret_value in secrets.values():
            assert secret_value not in payload_str, f'LEAKED: {secret_value}'

        # Verify encryption happened
        assert 'encrypted_credentials' in payload
        assert len(payload['encrypted_credentials']) > 100

    def test_wrong_key_cannot_decrypt(self, keypair: tuple[Any, Any]) -> None:
        """Attacker with different key MUST NOT decrypt."""
        _, public_key = keypair

        # Attacker's key
        attacker_key = rsa.generate_private_key(65537, 2048, default_backend())

        credentials = {'token': 'secret_value'}
        ciphertext = encrypt_credentials(public_key, credentials)
        ciphertext_bytes = _base64url_decode(ciphertext)

        # Attacker MUST fail
        with pytest.raises(Exception):
            attacker_key.decrypt(
                ciphertext_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

    def test_correct_key_decrypts(self, keypair: tuple[Any, Any]) -> None:
        """Holder of private key CAN decrypt."""
        private_key, public_key = keypair

        credentials = {'token': 'secret_value'}
        ciphertext = encrypt_credentials(public_key, credentials)
        ciphertext_bytes = _base64url_decode(ciphertext)

        plaintext = private_key.decrypt(
            ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        assert b'secret_value' in plaintext

    def test_oaep_randomization(self, keypair: tuple[Any, Any]) -> None:
        """Same plaintext MUST produce different ciphertext (OAEP)."""
        _, public_key = keypair
        credentials = {'token': 'same_value'}

        ct1 = encrypt_credentials(public_key, credentials)
        ct2 = encrypt_credentials(public_key, credentials)

        assert ct1 != ct2, 'Encryption not randomized - replay attacks possible'


# --- Invariant: Only encryption keys accepted. --------------------------------


class TestAlgorithmConfusionPrevention:
    """Signing keys MUST NOT be used for encryption."""

    @pytest.mark.asyncio
    async def test_signing_key_rejected(self) -> None:
        """JWKS with only use=sig keys MUST fail."""
        from dedalus_labs.lib.runner.encryption import fetch_encryption_public_key

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'keys': [
                {'kty': 'RSA', 'use': 'sig', 'kid': 'signing-key', 'n': 'x', 'e': 'y'},
                {'kty': 'EC', 'use': 'sig', 'kid': 'ec-key', 'crv': 'P-256'},
            ]
        }
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get = MagicMock(return_value=mock_response)

        # TODO: Test async version as well.
        # Sync version for simpler testing
        from dedalus_labs.lib.runner.encryption import fetch_encryption_public_key_sync

        with pytest.raises(ValueError, match='No RSA encryption key'):
            fetch_encryption_public_key_sync(mock_client, 'https://as.example.com')


# --- Invariant: Empty/malformed JWKS must be rejected. ------------------------


class TestJWKSResponseValidation:
    """Malformed JWKS responses MUST be rejected."""

    def test_empty_keys_rejected(self) -> None:
        """Empty keys array MUST fail."""
        from dedalus_labs.lib.runner.encryption import fetch_encryption_public_key_sync

        mock_response = MagicMock()
        mock_response.json.return_value = {'keys': []}
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError, match='No keys found'):
            fetch_encryption_public_key_sync(mock_client, 'https://as.example.com')

    def test_missing_keys_field_rejected(self) -> None:
        """JWKS without 'keys' field MUST fail."""
        from dedalus_labs.lib.runner.encryption import fetch_encryption_public_key_sync

        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError, match='No keys found'):
            fetch_encryption_public_key_sync(mock_client, 'https://as.example.com')


# 
# --- Invariant: Credential size limits. ---------------------------------------


class TestCredentialSizeLimits:
    """Credentials exceeding RSA-OAEP limit MUST fail clearly."""

    @pytest.fixture
    def keypair_3072(self) -> tuple[Any, Any]:
        private = rsa.generate_private_key(65537, 3072, default_backend())
        return private, private.public_key()

    def test_normal_credentials_work(self, keypair_3072: tuple[Any, Any]) -> None:
        """Normal-sized credentials encrypt successfully."""
        _, public_key = keypair_3072
        credentials = {'token': 'ghp_xxx123456789'}

        ciphertext = encrypt_credentials(public_key, credentials)
        assert len(ciphertext) > 0

    def test_oversized_credentials_fail(self, keypair_3072: tuple[Any, Any]) -> None:
        """Credentials exceeding RSA-OAEP limit MUST fail.

        3072-bit RSA with SHA-256 OAEP: max ~318 bytes plaintext.
        """
        _, public_key = keypair_3072

        # 400 bytes + JSON overhead exceeds limit
        large_value = 'x' * 400
        credentials = {'large_token': large_value}

        with pytest.raises(ValueError):
            encrypt_credentials(public_key, credentials)


# --- Invariant: Error messages must not leak secrets. -------------------------


class TestErrorMessageSecurity:
    """Error messages MUST NOT contain sensitive data."""

    def test_decryption_error_clean(self) -> None:
        """Failed decryption error MUST NOT reveal plaintext."""
        key1 = rsa.generate_private_key(65537, 2048, default_backend())
        key2 = rsa.generate_private_key(65537, 2048, default_backend())

        secret_value = 'NEVER_LEAK_THIS_IN_ERRORS'
        credentials = {'secret': secret_value}
        ciphertext = encrypt_credentials(key1.public_key(), credentials)
        ciphertext_bytes = _base64url_decode(ciphertext)

        try:
            key2.decrypt(
                ciphertext_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            pytest.fail('Decryption with wrong key should fail')
        except Exception as e:
            error_str = str(e)
            assert secret_value not in error_str, f'SECRET LEAKED IN ERROR: {error_str}'
