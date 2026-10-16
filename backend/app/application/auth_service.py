from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlencode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.clock import Clock
from app.core.config import Settings
from app.core.security import (
    InvalidAccessToken,
    create_access_token,
    digest_reset_token,
    generate_reset_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from app.db.models import AuthSession, PasswordResetToken, User
from app.domain.errors import AuthenticationError, ConflictError, InvalidResetTokenError
from app.infrastructure.email import EmailSender
from app.infrastructure.repositories import (
    AuthSessionRepository,
    PasswordResetTokenRepository,
    UserRepository,
)


@dataclass(frozen=True)
class AuthenticatedAccount:
    user: User
    auth_session: AuthSession


class AuthService:
    def __init__(
        self,
        session: Session,
        settings: Settings,
        clock: Clock,
        email_sender: EmailSender,
    ):
        self.session = session
        self.settings = settings
        self.clock = clock
        self.email_sender = email_sender
        self.users = UserRepository(session)
        self.sessions = AuthSessionRepository(session)
        self.reset_tokens = PasswordResetTokenRepository(session)

    def register(self, display_name: str, email: str, password: str) -> User:
        normalized_email = normalize_email(email)
        if self.users.get_by_email(normalized_email):
            raise ConflictError(
                "email_already_registered",
                "Ya existe una cuenta asociada a ese email",
            )
        user = User.new(
            display_name.strip(),
            normalized_email,
            hash_password(password),
            self.clock.now_utc(),
        )
        self.users.add(user)
        try:
            self.session.flush()
        except IntegrityError as exc:
            raise ConflictError(
                "email_already_registered",
                "Ya existe una cuenta asociada a ese email",
            ) from exc
        return user

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(normalize_email(email))
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationError("invalid_credentials", "Email o contraseña incorrectos")
        now = self.clock.now_utc()
        auth_session = AuthSession.new(user.id, now)
        self.sessions.add(auth_session)
        self.session.flush()
        return create_access_token(user.id, auth_session.id, self.settings, now)

    def authenticate(self, token: str) -> AuthenticatedAccount:
        try:
            claims = verify_access_token(token, self.settings, self.clock.now_utc())
        except InvalidAccessToken as exc:
            raise AuthenticationError() from exc
        auth_session = self.sessions.get(claims.session_id)
        now = self.clock.now_utc()
        if (
            auth_session is None
            or auth_session.user_id != claims.subject
            or auth_session.revoked_at is not None
            or _as_utc(auth_session.expires_at) <= now
        ):
            raise AuthenticationError()
        user = self.users.get(claims.subject)
        if user is None:
            raise AuthenticationError()
        return AuthenticatedAccount(user=user, auth_session=auth_session)

    def logout(self, authenticated: AuthenticatedAccount) -> None:
        authenticated.auth_session.revoked_at = self.clock.now_utc()

    def request_password_recovery(self, email: str) -> None:
        user = self.users.get_by_email(normalize_email(email))
        if user is None:
            return
        raw_token = generate_reset_token()
        token = PasswordResetToken.new(
            user.id,
            digest_reset_token(raw_token),
            self.clock.now_utc(),
        )
        self.reset_tokens.add(token)
        self.session.flush()
        separator = "&" if "?" in self.settings.reset_url_base else "?"
        reset_url = f"{self.settings.reset_url_base}{separator}{urlencode({'token': raw_token})}"
        self.email_sender.send_password_reset(user.email, reset_url)

    def reset_password(self, raw_token: str, new_password: str) -> None:
        token = self.reset_tokens.get_by_digest(digest_reset_token(raw_token))
        now = self.clock.now_utc()
        if token is None or token.used_at is not None or _as_utc(token.expires_at) <= now:
            raise InvalidResetTokenError()
        user = self.users.get(token.user_id)
        if user is None:
            raise InvalidResetTokenError()
        user.password_hash = hash_password(new_password)
        token.used_at = now
        self.reset_tokens.consume_other_unused(user.id, token.id, now)
        self.sessions.revoke_all_for_user(user.id, now)
        self.session.flush()


def normalize_email(email: str) -> str:
    return email.strip().lower()


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
