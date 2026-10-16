from __future__ import annotations

from datetime import datetime
from typing import Generic, Protocol, TypeVar

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models import AuthSession, PasswordResetToken, User


T = TypeVar("T")


class BoardScopedRepository(Protocol[T]):
    """Future board repositories must scope lookups by resource and board IDs."""

    def get_for_board(self, resource_id: str, board_id: str) -> T | None: ...


class SqlAlchemyBoardScopedRepository(Generic[T]):
    """Reusable scoped lookup; concrete board repositories provide their mapped model."""

    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get_for_board(self, resource_id: str, board_id: str) -> T | None:
        return self.session.scalar(
            select(self.model).where(
                getattr(self.model, "id") == resource_id,
                getattr(self.model, "board_id") == board_id,
            )
        )


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: str) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def add(self, user: User) -> None:
        self.session.add(user)


class AuthSessionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, session_id: str) -> AuthSession | None:
        return self.session.get(AuthSession, session_id)

    def add(self, auth_session: AuthSession) -> None:
        self.session.add(auth_session)

    def revoke_all_for_user(self, user_id: str, now: datetime) -> None:
        self.session.execute(
            update(AuthSession)
            .where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
            .values(revoked_at=now)
        )


class PasswordResetTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_digest(self, digest: str) -> PasswordResetToken | None:
        return self.session.scalar(
            select(PasswordResetToken).where(PasswordResetToken.token_digest == digest)
        )

    def add(self, token: PasswordResetToken) -> None:
        self.session.add(token)

    def consume_other_unused(self, user_id: str, current_id: str, now: datetime) -> None:
        self.session.execute(
            update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user_id,
                PasswordResetToken.id != current_id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(used_at=now)
        )
