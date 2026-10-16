from __future__ import annotations

from contextlib import asynccontextmanager
import json
import logging
from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.dependencies import install_error_handlers
from app.api.routers.auth import router as auth_router
from app.core.clock import Clock, SystemClock
from app.core.config import Settings, get_settings
from app.db.base import Base
from app.db.session import create_session_factory, create_sqlite_engine
from app.infrastructure.email import EmailSender, create_email_sender


logger = logging.getLogger("gestor_gastos")


def create_app(
    settings: Settings | None = None,
    clock: Clock | None = None,
    email_sender: EmailSender | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()
    engine = create_sqlite_engine(resolved_settings.database_url)
    session_factory = create_session_factory(engine)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        Base.metadata.create_all(engine)
        yield
        engine.dispose()

    application = FastAPI(title="Gestor de Gastos MVP API", lifespan=lifespan)
    application.state.settings = resolved_settings
    application.state.clock = clock or SystemClock()
    application.state.email_sender = email_sender or create_email_sender(resolved_settings)
    application.state.engine = engine
    application.state.session_factory = session_factory
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[resolved_settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    install_error_handlers(application)

    @application.middleware("http")
    async def structured_request_log(request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id") or str(uuid4())
        started = perf_counter()
        try:
            response = await call_next(request)
            outcome = response.status_code
        except Exception:
            outcome = 500
            raise
        finally:
            logger.info(
                json.dumps(
                    {
                        "correlation_id": correlation_id,
                        "route": request.url.path,
                        "outcome": outcome,
                        "duration_ms": round((perf_counter() - started) * 1000, 2),
                    }
                )
            )
        response.headers["x-correlation-id"] = correlation_id
        return response

    @application.get("/api/health", tags=["Health"])
    def health():
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok"}

    application.include_router(auth_router, prefix="/api")
    return application


class LazyApplication:
    def __init__(self) -> None:
        self._application: FastAPI | None = None

    async def __call__(self, scope: dict[str, Any], receive, send) -> None:
        if self._application is None:
            self._application = create_app()
        await self._application(scope, receive, send)


app = LazyApplication()
