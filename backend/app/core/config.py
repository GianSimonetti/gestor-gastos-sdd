from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    database_url: str = "sqlite:///./gestor_gastos.db"
    jwt_secret: SecretStr
    jwt_issuer: str = "gestor-gastos"
    jwt_audience: str = "gestor-gastos-web"
    invitation_secret: SecretStr
    app_timezone: str = "America/Argentina/Buenos_Aires"
    frontend_origin: str = "http://localhost:5173"
    reset_url_base: str = "http://localhost:5173/reset-password"
    email_backend: Literal["memory", "smtp"] = "memory"
    app_env: Literal["local", "test", "production"] = "local"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_sender: str | None = None
    smtp_username: str | None = None
    smtp_password: SecretStr | None = None
    smtp_use_tls: bool = True
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    whisper_local_only: bool = True

    @property
    def secure_cookies(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
