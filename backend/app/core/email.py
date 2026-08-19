"""Async email sender using aiosmtplib with retry logic and Jinja2 templates."""
from __future__ import annotations

import asyncio
import logging
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from backend.app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

# Template directory relative to this file: backend/app/templates/email
_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "email"

_env: Environment | None = None


def _get_jinja_env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(
            loader=FileSystemLoader(str(_TEMPLATE_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
        )
    return _env


def render_template(template_name: str, **context) -> str:
    """Render a Jinja2 email template."""
    env = _get_jinja_env()
    template = env.get_template(template_name)
    return template.render(**context)


async def _send_with_smtp(
    settings: Settings,
    message: EmailMessage,
) -> None:
    """Send a single EmailMessage via aiosmtplib with retry/backoff."""
    if settings.smtp_use_tls and settings.smtp_port == 465:
        smtp = aiosmtplib.SMTP(
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            use_tls=True,
        )
    else:
        smtp = aiosmtplib.SMTP(
            hostname=settings.smtp_host,
            port=settings.smtp_port,
        )

    last_exception: Exception | None = None
    for attempt in range(1, 4):
        try:
            await smtp.connect()
            if not settings.smtp_use_tls or settings.smtp_port == 587:
                try:
                    await smtp.starttls()
                except Exception:
                    pass  # Some servers may not support STARTTLS
            if settings.smtp_user and settings.smtp_password:
                await smtp.login(settings.smtp_user, settings.smtp_password)
            await smtp.send_message(message)
            await smtp.quit()
            return
        except Exception as exc:
            last_exception = exc
            logger.warning("SMTP attempt %s failed: %s", attempt, exc)
            if attempt < 3:
                backoff = 2 ** attempt
                await asyncio.sleep(backoff)

    if last_exception:
        raise last_exception


async def send_email(
    to: str,
    subject: str,
    html_body: str,
    text_body: str | None = None,
    from_addr: str | None = None,
) -> None:
    """Send a single HTML email (optionally with plain-text fallback)."""
    settings = get_settings()
    _from = from_addr or settings.smtp_from_email or settings.smtp_user or "noreply@example.com"

    message = EmailMessage()
    message["From"] = _from
    message["To"] = to
    message["Subject"] = subject

    if text_body:
        message.set_content(text_body)
        message.add_alternative(html_body, subtype="html")
    else:
        message.set_content(html_body, subtype="html")

    try:
        await _send_with_smtp(settings, message)
        logger.info("Email sent successfully to %s (subject: %s)", to, subject)
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        raise


async def send_bulk_email(
    recipients: Iterable[str],
    subject: str,
    html_body: str,
    text_body: str | None = None,
) -> tuple[int, list[str]]:
    """Send an email to multiple recipients. Returns (sent_count, failures)."""
    settings = get_settings()
    _from = settings.smtp_from_email or settings.smtp_user or "noreply@example.com"

    sent = 0
    failures: list[str] = []

    for recipient in recipients:
        message = EmailMessage()
        message["From"] = _from
        message["To"] = recipient
        message["Subject"] = subject

        if text_body:
            message.set_content(text_body)
            message.add_alternative(html_body, subtype="html")
        else:
            message.set_content(html_body, subtype="html")

        try:
            await _send_with_smtp(settings, message)
            sent += 1
            logger.info("Bulk email sent to %s", recipient)
        except Exception as exc:
            logger.error("Bulk email failed for %s: %s", recipient, exc)
            failures.append(recipient)

    logger.info("Bulk send complete: %s sent, %s failed", sent, len(failures))
    return sent, failures
