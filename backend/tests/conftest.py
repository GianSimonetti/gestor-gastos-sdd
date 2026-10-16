from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def settings(tmp_path):
    from app.core.config import Settings

    return Settings(
        database_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        jwt_secret="test-jwt-secret-that-is-deliberately-longer-than-sixty-four-bytes-for-tests",
        invitation_secret="test-invitation-secret-that-is-deliberately-longer-than-sixty-four-bytes",
        app_env="test",
        email_backend="memory",
        frontend_origin="http://testserver",
        reset_url_base="http://testserver/reset-password",
    )


@pytest.fixture
def mutable_clock():
    from app.core.clock import MutableClock

    return MutableClock(datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc))


@pytest.fixture
def email_sender():
    from app.infrastructure.email import MemoryEmailSender

    return MemoryEmailSender()


@pytest.fixture
def app(settings, mutable_clock, email_sender):
    from app.main import create_app

    return create_app(settings=settings, clock=mutable_clock, email_sender=email_sender)


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client
