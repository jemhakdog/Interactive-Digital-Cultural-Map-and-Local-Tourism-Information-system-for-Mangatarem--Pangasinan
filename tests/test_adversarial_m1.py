"""Adversarial stress tests for Milestone M1 (Authentication & Security Hardening).

Targets:
1. POST /api/auth/google
   - Forged JWTs signed with attacker RSA private keys (offline verification rejection)
   - Forged JWTs signed with attacker HMAC keys (algorithm confusion)
   - Invalid token issuers (spoofed domains, evil issuers, non-HTTPS)
   - Malformed, corrupted, truncated, and empty credentials
   - Expired tokens
   - Tokens with missing, empty, or null email claims
   - Tokens with email_verified=False (unverified email identities)

2. POST /api/auth/forgot-password & POST /api/auth/reset-password
   - Multiple reset requests for the same user (Token invalidation / replacement)
   - Prior reset tokens cannot be reused once superseded
   - Single-use token enforcement (replay attack prevention)
   - Password reset with expired or fabricated tokens
   - Input fuzzing (empty token, invalid length passwords, SQL injection characters)
"""
from __future__ import annotations

import base64
import json
import logging
import re
import secrets
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from google.auth.exceptions import GoogleAuthError
from jose import jwt


# ── Helper: Generate attacker RSA signed JWT ──────────────────────────────────
def _generate_attacker_rsa_jwt(payload: dict) -> str:
    """Generate an RS256 JWT signed with an attacker's generated RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    header = {"alg": "RS256", "typ": "JWT", "kid": "attacker-fake-key-id"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signing_input = f"{header_b64}.{payload_b64}".encode()
    from cryptography.hazmat.primitives.asymmetric import padding
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    return f"{header_b64}.{payload_b64}.{sig_b64}"


# ─────────────────────────────────────────────────────────────────────────────
# 1. Adversarial Attacks on POST /api/auth/google
# ─────────────────────────────────────────────────────────────────────────────

def test_google_auth_attacker_rsa_signed_jwt_rejected_with_401(client):
    """An attacker generates a valid RSA signed JWT with victim email.

    Since the key is not in Google's JWKS, it MUST be rejected with HTTP 401.
    """
    now = int(datetime.now(UTC).timestamp())
    payload = {
        "iss": "https://accounts.google.com",
        "aud": "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
        "sub": "attacker-generated-sub-999",
        "email": "victim_executive@mangatarem.gov.ph",
        "email_verified": True,
        "name": "Victim Executive",
        "iat": now,
        "exp": now + 3600,
    }
    attacker_jwt = _generate_attacker_rsa_jwt(payload)

    response = client.post("/api/auth/google", json={"credential": attacker_jwt})
    assert response.status_code == 401, (
        f"Expected 401 Unauthorized for forged RSA token, got {response.status_code}: {response.text}"
    )
    assert "Invalid Google OAuth credential" in response.json().get("detail", "")


def test_google_auth_hmac_alg_confusion_jwt_rejected_with_401(client):
    """An attacker crafts an HS256 HMAC-signed JWT.

    Google ID tokens are RS256/ES256; HMAC tokens must be rejected with HTTP 401.
    """
    now = int(datetime.now(UTC).timestamp())
    payload = {
        "iss": "https://accounts.google.com",
        "aud": "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
        "sub": "attacker-sub-hmac",
        "email": "admin@mangatarem.gov.ph",
        "email_verified": True,
        "iat": now,
        "exp": now + 3600,
    }
    hmac_token = jwt.encode(payload, "attacker-secret-key-12345", algorithm="HS256")

    response = client.post("/api/auth/google", json={"credential": hmac_token})
    assert response.status_code == 401, (
        f"Expected 401 for HMAC-signed token, got {response.status_code}: {response.text}"
    )
    assert "Invalid Google OAuth credential" in response.json().get("detail", "")


@pytest.mark.parametrize(
    "invalid_iss",
    [
        "https://evil-google.com",
        "https://accounts.google.com.attacker.com",
        "http://accounts.google.com",  # Non-HTTPS
        "accounts.google.com",         # Missing scheme
        "https://attacker-identity-provider.org",
        "",
    ],
)
def test_google_auth_invalid_issuers_rejected_with_401(client, invalid_iss):
    """Tokens with unauthorized issuers must be rejected with HTTP 401."""
    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        side_effect=GoogleAuthError(f"Invalid issuer: {invalid_iss}"),
    ):
        response = client.post("/api/auth/google", json={"credential": "token.with.bad.issuer"})
        assert response.status_code == 401
        assert "Invalid Google OAuth credential" in response.json().get("detail", "")


@pytest.mark.parametrize(
    "malformed_token",
    [
        "",                                     # Empty string
        "   ",                                  # Whitespace only
        "not-a-token",                          # Single segment
        "header.payload",                       # Missing signature segment
        "h.p.s.extra",                          # 4 segments
        "\x00\xff\xfe\x01\x02\x03",             # Binary non-ASCII garbage
        "eyJhbGciOiJSUzI1NiJ9.invalid-base64.sig", # Corrupt base64
        "A" * 10000,                            # Large payload flood
    ],
)
def test_google_auth_malformed_tokens_rejected_with_401(client, malformed_token):
    """Malformed and corrupted token payloads must consistently receive HTTP 401."""
    response = client.post("/api/auth/google", json={"credential": malformed_token})
    assert response.status_code == 401, (
        f"Malformed token '{malformed_token[:20]}...' returned {response.status_code}: {response.text}"
    )
    assert "Invalid Google OAuth credential" in response.json().get("detail", "")


def test_google_auth_expired_token_rejected_with_401(client):
    """Expired Google ID tokens must be rejected with HTTP 401."""
    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        side_effect=ValueError("Token used too late, 1729650000 < 1729653600"),
    ):
        response = client.post("/api/auth/google", json={"credential": "expired.jwt.token"})
        assert response.status_code == 401
        assert "Invalid Google OAuth credential" in response.json().get("detail", "")


@pytest.mark.parametrize(
    "idinfo_without_valid_email",
    [
        {"name": "No Email User", "sub": "uid-1"},                     # Missing email key
        {"email": None, "name": "Null Email User", "sub": "uid-2"},    # Null email
        {"email": "", "name": "Empty Email User", "sub": "uid-3"},      # Empty string email
    ],
)
def test_google_auth_missing_or_empty_email_rejected_with_401(client, idinfo_without_valid_email):
    """If Google idinfo lacks a valid email claim, authentication must be rejected with HTTP 401."""
    with patch(
        "google.oauth2.id_token.verify_oauth2_token",
        return_value=idinfo_without_valid_email,
    ):
        response = client.post("/api/auth/google", json={"credential": "token.with.missing.email"})
        assert response.status_code == 401, (
            f"Expected 401 for idinfo without email, got {response.status_code}: {response.text}"
        )
        assert "Invalid Google OAuth credential" in response.json().get("detail", "")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Adversarial Attacks on Password Reset (Token Invalidation & Replay)
# ─────────────────────────────────────────────────────────────────────────────

def _register_test_user(client, email: str, name: str, password: str = "initialPass123!"):
    """Helper: register a test user via public endpoint."""
    resp = client.post(
        "/api/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": "user",
        },
    )
    assert resp.status_code == 201, f"Failed to register test user: {resp.text}"
    return resp.json()


def _extract_token_from_caplog(caplog) -> str:
    """Extract password reset token from logger output."""
    for record in reversed(caplog.records):
        match = re.search(r"token=([a-f0-9]+)", record.message)
        if match:
            return match.group(1)
    raise ValueError(f"No reset token found in captured logs. Logs: {[r.message for r in caplog.records]}")


def test_password_reset_multiple_requests_invalidates_prior_tokens(client, caplog):
    """Multiple reset requests for the same user must invalidate all prior reset tokens.

    Attack Scenario:
    1. User requests password reset -> Token A generated.
    2. User (or attacker) requests another password reset -> Token B generated.
    3. Attacker discovers or intercepts Token A and attempts to reset password.
    4. Token A must be rejected with HTTP 400.
    5. Only the latest token (Token B) must be accepted.
    """
    caplog.set_level(logging.INFO)
    email = f"multi_reset_{secrets.token_hex(4)}@mangatarem.com"
    _register_test_user(client, email=email, name=f"User_{secrets.token_hex(4)}")

    # Request 1: Generate Token A
    resp1 = client.post("/api/auth/forgot-password", json={"email": email})
    assert resp1.status_code == 200
    token_a = _extract_token_from_caplog(caplog)
    assert len(token_a) >= 32

    # Request 2: Generate Token B
    resp2 = client.post("/api/auth/forgot-password", json={"email": email})
    assert resp2.status_code == 200
    token_b = _extract_token_from_caplog(caplog)
    assert len(token_b) >= 32
    assert token_a != token_b, "Subsequent forgot-password request must generate a distinct token"

    # Attacker attempts to use superseded Token A -> MUST FAIL with HTTP 400
    attack_resp = client.post(
        "/api/auth/reset-password",
        json={"token": token_a, "password": "attackerNewPassword1!"},
    )
    assert attack_resp.status_code == 400, (
        f"Prior token A should be invalidated, but got {attack_resp.status_code}: {attack_resp.text}"
    )
    assert "Invalid or expired reset token" in attack_resp.json().get("detail", "")

    # Legitimate user uses Token B -> MUST SUCCEED with HTTP 200
    success_resp = client.post(
        "/api/auth/reset-password",
        json={"token": token_b, "password": "legitNewPassword1!"},
    )
    assert success_resp.status_code == 200, (
        f"Latest token B should succeed, got {success_resp.status_code}: {success_resp.text}"
    )

    # Verify login with new password succeeds
    login_resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": "legitNewPassword1!"},
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


def test_password_reset_single_use_token_replay_attack_rejected(client, caplog):
    """A reset token cannot be reused after being successfully consumed (replay attack prevention).

    Scenario:
    1. User requests reset -> Token generated.
    2. User resets password -> HTTP 200.
    3. Attacker replays the same token with a different password -> HTTP 400.
    """
    caplog.set_level(logging.INFO)
    email = f"single_use_{secrets.token_hex(4)}@mangatarem.com"
    _register_test_user(client, email=email, name=f"User_{secrets.token_hex(4)}")

    resp = client.post("/api/auth/forgot-password", json={"email": email})
    assert resp.status_code == 200
    token = _extract_token_from_caplog(caplog)

    # First consumption succeeds
    use_resp = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "brandNewPassword123!"},
    )
    assert use_resp.status_code == 200

    # Replay attack with same token must fail
    replay_resp = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "maliciousHijackPassword123!"},
    )
    assert replay_resp.status_code == 400, (
        f"Replay of consumed token must return 400, got {replay_resp.status_code}: {replay_resp.text}"
    )
    assert "Invalid or expired reset token" in replay_resp.json().get("detail", "")

    # Confirm password remains brandNewPassword123!
    ok_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "brandNewPassword123!"},
    )
    assert ok_login.status_code == 200

    hijack_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "maliciousHijackPassword123!"},
    )
    assert hijack_login.status_code == 401


@pytest.mark.parametrize(
    "invalid_token",
    [
        "nonexistent_token_0123456789abcdef",
        "0" * 64,
        "f" * 64,
        "' OR '1'='1' --",                       # SQL Injection attempt
        "'; DROP TABLE \"USER\"; --",            # DDL injection attempt
        "token\x00with_null_bytes",              # Null byte injection
    ],
)
def test_password_reset_fabricated_or_injection_tokens_rejected_with_400(client, invalid_token):
    """Fabricated or SQL injection tokens must be rejected with HTTP 400."""
    response = client.post(
        "/api/auth/reset-password",
        json={"token": invalid_token, "password": "validNewPassword123!"},
    )
    assert response.status_code == 400
    assert "Invalid or expired reset token" in response.json().get("detail", "")


@pytest.mark.parametrize(
    "weak_password,expected_code",
    [
        ("", 422),           # Empty password (min length violation)
        ("12345", 422),      # 5 chars (min length 6)
        ("A" * 129, 422),    # 129 chars (max length 128)
    ],
)
def test_password_reset_password_length_boundaries_rejected(client, weak_password, expected_code):
    """Passwords violating length constraints (6-128) must be rejected with 422 Unprocessable Entity."""
    response = client.post(
        "/api/auth/reset-password",
        json={"token": "some_random_token_1234567890", "password": weak_password},
    )
    assert response.status_code == expected_code


def test_forgot_password_anti_enumeration_behavior(client):
    """Forgot password must not disclose account existence or leak user metadata."""
    resp_exist = client.post("/api/auth/forgot-password", json={"email": "existing_account@example.com"})
    resp_nonexist = client.post("/api/auth/forgot-password", json={"email": "completely_fake_account_99999@example.com"})

    assert resp_exist.status_code == 200
    assert resp_nonexist.status_code == 200
    # Both responses must return the exact same generic message
    assert resp_exist.json() == resp_nonexist.json()


def test_google_auth_unverified_email_rejected_with_401(client):
    """Empirical challenge: Tokens with email_verified=False must be rejected with HTTP 401.

    Google ID tokens for unverified emails contain email_verified=False.
    If the backend does not enforce email_verified=True, an attacker can register an
    unverified Google account with a victim's email address and take over their account.
    """
    mock_idinfo = {
        "email": "unverified_victim@mangatarem.gov.ph",
        "name": "Unverified User",
        "email_verified": False,
        "sub": "unverified-sub-12345",
    }
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_idinfo):
        response = client.post("/api/auth/google", json={"credential": "valid.signed.but.unverified.email"})
        assert response.status_code == 401, (
            f"Vulnerability reproduced: Token with email_verified=False was accepted with HTTP {response.status_code}"
        )


def test_password_reset_concurrent_race_condition(client, caplog):
    """Empirical challenge: Two concurrent HTTP requests attempting to redeem the same reset token.

    Under strict serializability and single-use token constraints, exactly ONE request
    must receive HTTP 200 and the competing concurrent request must receive HTTP 400.
    """
    import concurrent.futures

    caplog.set_level(logging.INFO)
    email = f"race_reset_{secrets.token_hex(4)}@mangatarem.com"
    _register_test_user(client, email=email, name=f"User_{secrets.token_hex(4)}")

    resp = client.post("/api/auth/forgot-password", json={"email": email})
    assert resp.status_code == 200
    token = _extract_token_from_caplog(caplog)

    def _attempt_reset(new_password):
        return client.post(
            "/api/auth/reset-password",
            json={"token": token, "password": new_password},
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(_attempt_reset, "ConcurrentPassA1!")
        f2 = executor.submit(_attempt_reset, "ConcurrentPassB2!")
        r1 = f1.result()
        r2 = f2.result()

    status_codes = sorted([r1.status_code, r2.status_code])
    # A hardened endpoint must enforce single-use even under race conditions:
    assert status_codes == [200, 400], (
        f"Vulnerability reproduced: Concurrent double-spend permitted. Statuses: {status_codes}"
    )


