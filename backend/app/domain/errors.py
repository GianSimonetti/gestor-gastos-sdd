from __future__ import annotations


class AppError(Exception):
    status_code = 400
    code = "application_error"
    default_message = "No se pudo completar la operación"

    def __init__(
        self,
        code: str | None = None,
        message: str | None = None,
        field_errors: dict[str, list[str]] | None = None,
    ):
        super().__init__(message or self.default_message)
        self.code = code or self.code
        self.message = message or self.default_message
        self.field_errors = field_errors


class DomainValidationError(AppError):
    status_code = 422
    code = "validation_error"
    default_message = "Los datos enviados no son válidos"


class AuthenticationError(AppError):
    status_code = 401
    code = "unauthorized"
    default_message = "Se requiere autenticación"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
    default_message = "El recurso entra en conflicto con el estado actual"


class InvalidResetTokenError(AppError):
    status_code = 400
    code = "invalid_reset_token"
    default_message = "El mecanismo de recuperación no es válido o ya venció"


class ResourceUnavailableError(AppError):
    status_code = 404
    code = "resource_unavailable"
    default_message = "El recurso no está disponible"
