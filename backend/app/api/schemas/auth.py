from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator


Password = Annotated[str, StringConstraints(min_length=8)]


class RegisterRequest(BaseModel):
    display_name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    email: EmailStr
    password: Password

    @field_validator("display_name")
    @classmethod
    def normalize_display_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("El nombre visible es obligatorio")
        return normalized


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PasswordRecoveryRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    token: Annotated[str, StringConstraints(min_length=40)]
    new_password: Password


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    display_name: str
    email: EmailStr


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    field_errors: dict[str, list[str]] | None = Field(default=None)
