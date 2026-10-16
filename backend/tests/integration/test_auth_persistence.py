from datetime import timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from app.db.base import Base
from app.db.models import AuthSession, PasswordResetToken, User
from app.db.session import create_session_factory, create_sqlite_engine, session_scope


def make_factory(tmp_path):
    engine = create_sqlite_engine(f"sqlite:///{(tmp_path / 'auth.db').as_posix()}")
    Base.metadata.create_all(engine)
    return create_session_factory(engine)


def test_normalized_email_is_unique(tmp_path):
    factory = make_factory(tmp_path)
    with session_scope(factory) as session:
        session.add(User.new("Carla", "carla@example.com", "hash"))

    with pytest.raises(IntegrityError):
        with session_scope(factory) as session:
            session.add(User.new("Otra", "carla@example.com", "hash"))


def test_sessions_and_reset_tokens_preserve_revocation_state(tmp_path, mutable_clock):
    factory = make_factory(tmp_path)
    now = mutable_clock.now_utc()
    with session_scope(factory) as session:
        user = User.new("Carla", "carla@example.com", "hash")
        session.add(user)
        session.flush()
        auth_session = AuthSession.new(user.id, now)
        reset = PasswordResetToken.new(user.id, "a" * 64, now)
        session.add_all([auth_session, reset])

    with session_scope(factory) as session:
        stored_session = session.query(AuthSession).one()
        stored_reset = session.query(PasswordResetToken).one()
        stored_session.revoked_at = now + timedelta(minutes=1)
        stored_reset.used_at = now + timedelta(minutes=1)

    with session_scope(factory) as session:
        assert session.query(AuthSession).one().revoked_at is not None
        assert session.query(PasswordResetToken).one().used_at is not None
