from __future__ import annotations

from dataclasses import dataclass
from email.message import EmailMessage
import smtplib
from typing import Protocol

from app.core.config import Settings


@dataclass(frozen=True)
class ResetEmail:
    recipient: str
    reset_url: str


class EmailSender(Protocol):
    def send_password_reset(self, recipient: str, reset_url: str) -> None: ...


class MemoryEmailSender:
    def __init__(self) -> None:
        self.outbox: list[ResetEmail] = []

    def send_password_reset(self, recipient: str, reset_url: str) -> None:
        self.outbox.append(ResetEmail(recipient=recipient, reset_url=reset_url))


class SmtpEmailSender:
    def __init__(self, settings: Settings):
        if not settings.smtp_host or not settings.smtp_sender:
            raise ValueError("SMTP host and sender are required")
        self.settings = settings

    def send_password_reset(self, recipient: str, reset_url: str) -> None:
        message = EmailMessage()
        message["Subject"] = "Recuperá tu acceso a Gestor de Gastos"
        message["From"] = self.settings.smtp_sender
        message["To"] = recipient
        message.set_content(
            "Usá el siguiente enlace dentro de los próximos 30 minutos:\n\n"
            f"{reset_url}\n\nSi no lo solicitaste, ignorá este mensaje."
        )
        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port, timeout=10) as smtp:
            if self.settings.smtp_use_tls:
                smtp.starttls()
            if self.settings.smtp_username and self.settings.smtp_password:
                smtp.login(
                    self.settings.smtp_username,
                    self.settings.smtp_password.get_secret_value(),
                )
            smtp.send_message(message)


def create_email_sender(settings: Settings) -> EmailSender:
    if settings.email_backend == "smtp":
        return SmtpEmailSender(settings)
    return MemoryEmailSender()
