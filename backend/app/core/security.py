from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import secrets

import jwt
from pwdlib import PasswordHash

from app.core.config import Settings


_PASSWORD_HASH = PasswordHash.recommended()
_ALGORITHM = "HS256"


class InvalidAccessToken(ValueError):
    pass


@dataclass(frozen=True)
class AccessClaims:
    subject: str
    session_id: str
    issued_at: datetime
    expires_at: datetime


def hash_password(password: str) -> str:
    return _PASSWORD_HASH.hash(password)


def verify_password(password: str, encoded: str) -> bool:
    try:
        return _PASSWORD_HASH.verify(password, encoded)
    except Exception:
        return False


def create_access_token(user_id: str, session_id: str, settings: Settings, now: datetime) -> str:
    expires_at = now + timedelta(minutes=30)
    return jwt.encode(
        {
            "sub": user_id,
            "jti": session_id,
            "iat": now,
            "exp": expires_at,
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
        },
        settings.jwt_secret.get_secret_value(),
        algorithm=_ALGORITHM,
    )


def verify_access_token(token: str, settings: Settings, now: datetime) -> AccessClaims:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[_ALGORITHM],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"require": ["sub", "jti", "iat", "exp"], "verify_exp": False},
        )
        issued_at = datetime.fromtimestamp(payload["iat"], timezone.utc)
        expires_at = datetime.fromtimestamp(payload["exp"], timezone.utc)
        if expires_at <= now.astimezone(timezone.utc):
            raise InvalidAccessToken("expired")
        return AccessClaims(payload["sub"], payload["jti"], issued_at, expires_at)
    except (jwt.PyJWTError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, InvalidAccessToken):
            raise
        raise InvalidAccessToken("invalid token") from exc


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def digest_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
