# ==============================================================================
#                  © 2025 Dedalus Labs, Inc. and affiliates
#                            Licensed under MIT
#           github.com/dedalus-labs/dedalus-sdk-python/LICENSE
# ==============================================================================

"""Tests for DPoP and Bearer auth handlers."""

from __future__ import annotations

from typing import Any

import pytest

# Skip if cryptography not installed
pytest.importorskip("cryptography")
pytest.importorskip("jwt")

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import jwt
import httpx

from dedalus_labs.lib.auth import (
    DPoPAuth,
    BearerAuth,
    generate_dpop_proof,
)


# --- Fixtures ---


@pytest.fixture
def ec_keypair() -> tuple[Any, Any]:
    """Generate P-256 keypair for DPoP testing."""
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture
def access_token() -> str:
    """Sample access token."""
    return "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.test_token"


# --- DPoP Proof Generation Tests ---


class TestGenerateDPoPProof:
    """Test DPoP proof JWT generation."""

    def test_basic_proof_structure(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof has correct JWT structure."""
        private_key, _ = ec_keypair

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="POST",
            url="https://api.example.com/token",
        )

        # Should be a valid JWT
        assert proof.count(".") == 2

        # Decode header (unverified) to check structure
        header = jwt.get_unverified_header(proof)
        assert header["typ"] == "dpop+jwt"
        assert header["alg"] == "ES256"
        assert "jwk" in header
        assert header["jwk"]["kty"] == "EC"
        assert header["jwk"]["crv"] == "P-256"

    def test_proof_claims(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof contains required claims."""
        private_key, public_key = ec_keypair

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="GET",
            url="https://api.example.com/resource?query=1",
        )

        # Decode and verify
        payload = jwt.decode(proof, public_key, algorithms=["ES256"])

        assert payload["htm"] == "GET"
        # URL should have query stripped
        assert payload["htu"] == "https://api.example.com/resource"
        assert "jti" in payload  # Unique ID
        assert "iat" in payload  # Issued at

    def test_proof_with_access_token(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof includes ath claim when access token provided."""
        private_key, public_key = ec_keypair
        token = "my_access_token"

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="POST",
            url="https://api.example.com/mcp",
            access_token=token,
        )

        payload = jwt.decode(proof, public_key, algorithms=["ES256"])
        assert "ath" in payload  # Access token hash

    def test_proof_with_nonce(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof includes nonce when provided."""
        private_key, public_key = ec_keypair

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="POST",
            url="https://api.example.com/token",
            nonce="server_nonce_123",
        )

        payload = jwt.decode(proof, public_key, algorithms=["ES256"])
        assert payload["nonce"] == "server_nonce_123"

    def test_each_proof_unique_jti(self, ec_keypair: tuple[Any, Any]) -> None:
        """Each proof has unique jti (replay prevention)."""
        private_key, public_key = ec_keypair

        proof1 = generate_dpop_proof(private_key, "GET", "https://api.example.com")
        proof2 = generate_dpop_proof(private_key, "GET", "https://api.example.com")

        payload1 = jwt.decode(proof1, public_key, algorithms=["ES256"])
        payload2 = jwt.decode(proof2, public_key, algorithms=["ES256"])

        assert payload1["jti"] != payload2["jti"]


# --- DPoPAuth Handler Tests ---


class TestDPoPAuth:
    """Test DPoP httpx.Auth handler."""

    def test_auth_flow_adds_headers(
        self, ec_keypair: tuple[Any, Any], access_token: str
    ) -> None:
        """Auth flow adds Authorization and DPoP headers."""
        private_key, _ = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)

        # Create a mock request
        request = httpx.Request("POST", "https://api.example.com/mcp")

        # Run auth flow
        flow = auth.auth_flow(request)
        modified_request = next(flow)

        # Check headers
        assert "Authorization" in modified_request.headers
        assert modified_request.headers["Authorization"].startswith("DPoP ")
        assert "DPoP" in modified_request.headers

    def test_authorization_uses_dpop_scheme(
        self, ec_keypair: tuple[Any, Any], access_token: str
    ) -> None:
        """Authorization header uses 'DPoP' scheme, not 'Bearer'."""
        private_key, _ = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)
        request = httpx.Request("GET", "https://api.example.com/resource")

        flow = auth.auth_flow(request)
        modified_request = next(flow)

        auth_header = modified_request.headers["Authorization"]
        assert auth_header.startswith("DPoP ")
        assert not auth_header.startswith("Bearer ")
        assert access_token in auth_header

    def test_proof_matches_request(
        self, ec_keypair: tuple[Any, Any], access_token: str
    ) -> None:
        """DPoP proof matches the actual request method and URL."""
        private_key, public_key = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)
        request = httpx.Request("DELETE", "https://api.example.com/item/123")

        flow = auth.auth_flow(request)
        modified_request = next(flow)

        # Decode the proof
        proof_jwt = modified_request.headers["DPoP"]
        payload = jwt.decode(proof_jwt, public_key, algorithms=["ES256"])

        assert payload["htm"] == "DELETE"
        assert payload["htu"] == "https://api.example.com/item/123"

    def test_set_nonce(self, ec_keypair: tuple[Any, Any], access_token: str) -> None:
        """Nonce can be updated after 401 response."""
        private_key, public_key = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)

        # Simulate server returning nonce
        auth.set_nonce("new_server_nonce")

        request = httpx.Request("POST", "https://api.example.com/mcp")
        flow = auth.auth_flow(request)
        modified_request = next(flow)

        proof_jwt = modified_request.headers["DPoP"]
        payload = jwt.decode(proof_jwt, public_key, algorithms=["ES256"])

        assert payload["nonce"] == "new_server_nonce"

    def test_thumbprint_property(self, ec_keypair: tuple[Any, Any]) -> None:
        """Thumbprint property returns JWK thumbprint."""
        private_key, _ = ec_keypair

        auth = DPoPAuth(access_token="token", dpop_key=private_key)

        thumbprint = auth.thumbprint
        # Should be base64url encoded SHA-256 (43 chars without padding)
        assert len(thumbprint) == 43
        assert all(c.isalnum() or c in "-_" for c in thumbprint)


# --- BearerAuth Tests ---


class TestBearerAuth:
    """Test simple Bearer token auth."""

    def test_adds_bearer_header(self) -> None:
        """Adds standard Bearer authorization header."""
        auth = BearerAuth(access_token="my_token")
        request = httpx.Request("GET", "https://api.example.com")

        flow = auth.auth_flow(request)
        modified_request = next(flow)

        assert modified_request.headers["Authorization"] == "Bearer my_token"

    def test_set_access_token(self) -> None:
        """Token can be updated after refresh."""
        auth = BearerAuth(access_token="old_token")
        auth.set_access_token("new_token")

        request = httpx.Request("GET", "https://api.example.com")
        flow = auth.auth_flow(request)
        modified_request = next(flow)

        assert modified_request.headers["Authorization"] == "Bearer new_token"
