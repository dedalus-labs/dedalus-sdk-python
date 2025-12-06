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

from dedalus_labs.auth import (
    DPoPAuth,
    BearerAuth,
    create_dpop_keypair,
)
from dedalus_labs.lib.auth import generate_dpop_proof  # Internal, for testing


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
    """Test DPoP proof JWT generation per RFC 9449."""

    def test_basic_proof_structure(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof has correct JWT structure with embedded JWK."""
        private_key, _ = ec_keypair

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="POST",
            url="https://api.example.com/token",
        )

        # Should be a valid JWT (header.payload.signature)
        assert proof.count(".") == 2

        header = jwt.get_unverified_header(proof)
        assert header["typ"] == "dpop+jwt"
        assert header["alg"] == "ES256"
        assert "jwk" in header
        assert header["jwk"]["kty"] == "EC"
        assert header["jwk"]["crv"] == "P-256"

    def test_proof_claims(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof contains required claims per RFC 9449 §4.2."""
        private_key, public_key = ec_keypair

        proof = generate_dpop_proof(
            dpop_key=private_key,
            method="GET",
            url="https://api.example.com/resource?query=1",
        )

        payload = jwt.decode(proof, public_key, algorithms=["ES256"])

        assert payload["htm"] == "GET"
        # URL should have query stripped per RFC 9449 §4.2
        assert payload["htu"] == "https://api.example.com/resource"
        assert "jti" in payload  # Unique ID for replay prevention
        assert "iat" in payload  # Issued at timestamp

    def test_proof_with_access_token(self, ec_keypair: tuple[Any, Any]) -> None:
        """Proof includes ath claim when access token provided (RFC 9449 §6.1)."""
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
        """Proof includes nonce when provided (server-provided nonce)."""
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
        """Each proof has unique jti for replay prevention."""
        private_key, public_key = ec_keypair

        proof1 = generate_dpop_proof(private_key, "GET", "https://api.example.com")
        proof2 = generate_dpop_proof(private_key, "GET", "https://api.example.com")

        payload1 = jwt.decode(proof1, public_key, algorithms=["ES256"])
        payload2 = jwt.decode(proof2, public_key, algorithms=["ES256"])

        assert payload1["jti"] != payload2["jti"]


# --- DPoPAuth Handler Tests ---


class TestDPoPAuth:
    """Test DPoP httpx.Auth handler.

    The auth_flow method is a sync generator per httpx.Auth contract.
    It works correctly with both sync and async httpx clients.
    """

    def test_auth_flow_adds_headers(
        self, ec_keypair: tuple[Any, Any], access_token: str
    ) -> None:
        """Auth flow adds Authorization and DPoP headers."""
        private_key, _ = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)
        request = httpx.Request("POST", "https://api.example.com/mcp")

        flow = auth.auth_flow(request)
        modified_request = next(flow)

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

        proof_jwt = modified_request.headers["DPoP"]
        payload = jwt.decode(proof_jwt, public_key, algorithms=["ES256"])

        assert payload["htm"] == "DELETE"
        assert payload["htu"] == "https://api.example.com/item/123"

    def test_set_nonce(self, ec_keypair: tuple[Any, Any], access_token: str) -> None:
        """Nonce can be updated after 401 response with DPoP-Nonce header."""
        private_key, public_key = ec_keypair

        auth = DPoPAuth(access_token=access_token, dpop_key=private_key)
        auth.set_nonce("new_server_nonce")

        request = httpx.Request("POST", "https://api.example.com/mcp")
        flow = auth.auth_flow(request)
        modified_request = next(flow)

        proof_jwt = modified_request.headers["DPoP"]
        payload = jwt.decode(proof_jwt, public_key, algorithms=["ES256"])

        assert payload["nonce"] == "new_server_nonce"

    def test_thumbprint_property(self, ec_keypair: tuple[Any, Any]) -> None:
        """Thumbprint property returns JWK thumbprint per RFC 7638."""
        private_key, _ = ec_keypair

        auth = DPoPAuth(access_token="token", dpop_key=private_key)

        thumbprint = auth.thumbprint
        # Base64url encoded SHA-256 (43 chars without padding)
        assert len(thumbprint) == 43
        assert all(c.isalnum() or c in "-_" for c in thumbprint)


# --- BearerAuth Tests ---


class TestBearerAuth:
    """Test simple Bearer token auth for servers without DPoP support."""

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


# --- Keypair Generation Tests ---


class TestCreateDPoPKeypair:
    """Test ephemeral keypair generation."""

    def test_generates_p256_key(self) -> None:
        """Creates valid P-256 EC key."""
        key = create_dpop_keypair()

        # Verify it's an EC key with correct curve
        assert hasattr(key, "public_key")
        public = key.public_key()
        assert public.curve.name == "secp256r1"

    def test_each_call_unique(self) -> None:
        """Each call generates a distinct keypair."""
        key1 = create_dpop_keypair()
        key2 = create_dpop_keypair()

        # Different public key coordinates
        pub1 = key1.public_key().public_numbers()
        pub2 = key2.public_key().public_numbers()

        assert pub1.x != pub2.x or pub1.y != pub2.y


# --- Token Exchange Tests (mocked AS) ---


from respx import MockRouter

from dedalus_labs.auth import create_dpop_auth, create_dpop_auth_sync

MOCK_AS_URL = "https://mock-as.test"


class TestCreateDPoPAuthSync:
    """Test sync token exchange with mocked AS."""

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    def test_token_exchange_success(self, respx_mock: MockRouter) -> None:
        """Successful token exchange returns configured DPoPAuth."""
        respx_mock.post("/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "dpop_bound_token_123", "token_type": "DPoP"},
            )
        )

        auth = create_dpop_auth_sync(api_key="dsk_test", as_url=MOCK_AS_URL)

        assert isinstance(auth, DPoPAuth)
        # Verify the auth handler has the returned token
        request = httpx.Request("GET", "https://api.example.com")
        flow = auth.auth_flow(request)
        modified = next(flow)
        assert "dpop_bound_token_123" in modified.headers["Authorization"]

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    def test_token_exchange_includes_dpop_proof(self, respx_mock: MockRouter) -> None:
        """Token request includes DPoP proof header."""
        captured_request = None

        def capture_request(request: httpx.Request) -> httpx.Response:
            nonlocal captured_request
            captured_request = request
            return httpx.Response(200, json={"access_token": "tok"})

        respx_mock.post("/token").mock(side_effect=capture_request)

        create_dpop_auth_sync(api_key="dsk_test", as_url=MOCK_AS_URL)

        assert captured_request is not None
        assert "DPoP" in captured_request.headers
        # Verify it's a valid JWT
        proof = captured_request.headers["DPoP"]
        assert proof.count(".") == 2

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    def test_token_exchange_sends_correct_grant(self, respx_mock: MockRouter) -> None:
        """Token request uses token-exchange grant type."""
        captured_request = None

        def capture_request(request: httpx.Request) -> httpx.Response:
            nonlocal captured_request
            captured_request = request
            return httpx.Response(200, json={"access_token": "tok"})

        respx_mock.post("/token").mock(side_effect=capture_request)

        create_dpop_auth_sync(api_key="dsk_my_key", as_url=MOCK_AS_URL)

        assert captured_request is not None
        body = captured_request.content.decode()
        assert "grant_type=urn" in body
        assert "token-exchange" in body
        assert "subject_token=dsk_my_key" in body

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    def test_nonce_from_response_header(self, respx_mock: MockRouter) -> None:
        """DPoP-Nonce response header is captured."""
        respx_mock.post("/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "tok"},
                headers={"DPoP-Nonce": "server_nonce_abc"},
            )
        )

        auth = create_dpop_auth_sync(api_key="dsk_test", as_url=MOCK_AS_URL)

        # Make a request and check nonce is in proof
        request = httpx.Request("GET", "https://api.example.com")
        flow = auth.auth_flow(request)
        modified = next(flow)

        proof = modified.headers["DPoP"]
        # Decode without verification (we don't have the key here)
        payload = jwt.decode(proof, options={"verify_signature": False})
        assert payload.get("nonce") == "server_nonce_abc"


class TestCreateDPoPAuthAsync:
    """Test async token exchange with mocked AS."""

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    async def test_token_exchange_success(self, respx_mock: MockRouter) -> None:
        """Successful async token exchange returns configured DPoPAuth."""
        respx_mock.post("/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "async_dpop_token", "token_type": "DPoP"},
            )
        )

        auth = await create_dpop_auth(api_key="dsk_test", as_url=MOCK_AS_URL)

        assert isinstance(auth, DPoPAuth)
        request = httpx.Request("POST", "https://api.example.com/mcp")
        flow = auth.auth_flow(request)
        modified = next(flow)
        assert "async_dpop_token" in modified.headers["Authorization"]

    @pytest.mark.respx(base_url=MOCK_AS_URL)
    async def test_error_response_raises(self, respx_mock: MockRouter) -> None:
        """HTTP error from AS raises exception."""
        respx_mock.post("/token").mock(
            return_value=httpx.Response(401, json={"error": "invalid_client"})
        )

        with pytest.raises(httpx.HTTPStatusError):
            await create_dpop_auth(api_key="bad_key", as_url=MOCK_AS_URL)
