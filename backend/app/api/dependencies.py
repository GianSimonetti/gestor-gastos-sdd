from __future__ import annotations

from collections.abc import Iterator

from fastapi import Cookie, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.application.auth_service import AuthService, AuthenticatedAccount
from app.core.clock import Clock
from app.core.config import Settings
from app.domain.errors import AppError, AuthenticationError
from app.infrastructure.email import EmailSender


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
        payload: dict[str, object] = {"code": exc.code, "message": exc.message}
        if exc.field_errors is not None:
            payload["field_errors"] = exc.field_errors
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        field_errors: dict[str, list[str]] = {}
        for error in exc.errors():
            location = [str(part) for part in error["loc"] if part not in {"body", "query", "path"}]
            field = ".".join(location) or "request"
            field_errors.setdefault(field, []).append(error["msg"])
        return JSONResponse(
            status_code=422,
            content={
                "code": "validation_error",
                "message": "Los datos enviados no son válidos",
                "field_errors": field_errors,
            },
        )


def get_session(request: Request) -> Iterator[Session]:
    session = request.app.state.session_factory()
    try:
        with session.begin():
            yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_auth_service(request: Request, session: Session = Depends(get_session)) -> AuthService:
    return AuthService(
        session=session,
        settings=request.app.state.settings,
        clock=request.app.state.clock,
        email_sender=request.app.state.email_sender,
    )


def require_authenticated_account(
    access_token: str | None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
) -> AuthenticatedAccount:
    if not access_token:
        raise AuthenticationError()
    return service.authenticate(access_token)


def app_settings(request: Request) -> Settings:
    return request.app.state.settings


def app_clock(request: Request) -> Clock:
    return request.app.state.clock


def app_email_sender(request: Request) -> EmailSender:
    return request.app.state.email_sender
