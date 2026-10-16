from datetime import timedelta

import jwt
import pytest

from app.core.security import (
    InvalidAccessToken,
    create_access_token,
    digest_reset_token,
    generate_reset_token,
    hash_password,
    verify_access_token,
    verify_password,
)


def test_password_is_argon2_hashed_and_verifiable():
    encoded = hash_password("correct horse battery staple")

    assert encoded != "correct horse battery staple"
    assert encoded.startswith("$argon2")
    assert verify_password("correct horse battery staple", encoded)
    assert not verify_password("wrong password", encoded)


def test_access_token_uses_fixed_claims_and_30_minute_expiry(settings, mutable_clock):
    token = create_access_token("user-id", "session-id", settings, mutable_clock.now_utc())
    claims = verify_access_token(token, settings, mutable_clock.now_utc())

    assert claims.subject == "user-id"
    assert claims.session_id == "session-id"
    assert claims.expires_at - claims.issued_at == timedelta(minutes=30)


def test_expired_and_wrong_algorithm_tokens_are_rejected(settings, mutable_clock):
    token = create_access_token("user-id", "session-id", settings, mutable_clock.now_utc())
    mutable_clock.advance(minutes=30)
    with pytest.raises(InvalidAccessToken):
        verify_access_token(token, settings, mutable_clock.now_utc())

    forged = jwt.encode(
        {"sub": "user-id", "jti": "session-id"},
        settings.jwt_secret.get_secret_value(),
        algorithm="HS512",
    )
    with pytest.raises(InvalidAccessToken):
        verify_access_token(forged, settings, mutable_clock.now_utc())


def test_reset_token_is_random_and_only_digest_is_stable():
    first = generate_reset_token()
    second = generate_reset_token()

    assert first != second
    assert len(first) >= 40
    assert first not in digest_reset_token(first)
    assert digest_reset_token(first) == digest_reset_token(first)
