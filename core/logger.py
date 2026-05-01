"""
Centralized logging helper for structured log messages.

Provides consistent logging with module/function context for debugging
and production monitoring.
"""

import logging

logger = logging.getLogger(__name__)


def log_entry(module: str, function: str, **kwargs) -> None:
    """Log function entry with optional context parameters."""
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    message = f"[{module}] > {function} > ENTRY"
    if context:
        message += f": {context}"
    logger.info(message)


def log_query(module: str, function: str, description: str) -> None:
    """Log database query or data fetching operation."""
    logger.debug("[%s] > %s > QUERY: %s", module, function, description)


def log_logic(module: str, function: str, decision: str) -> None:
    """Log business logic decision or conditional branch."""
    logger.debug("[%s] > %s > LOGIC: %s", module, function, decision)


def log_success(module: str, function: str, message_text: str) -> None:
    """Log successful operation completion."""
    logger.info("[%s] > %s > SUCCESS: %s", module, function, message_text)


def log_error(module: str, function: str, error_message: str) -> None:
    """Log error or validation failure."""
    logger.error("[%s] > %s > ERROR: %s", module, function, error_message)


def log_render(module: str, function: str, template: str) -> None:
    """Log template rendering operation."""
    logger.debug("[%s] > %s > RENDER: Rendering %s", module, function, template)


def log_redirect(module: str, function: str, destination: str) -> None:
    """Log HTTP redirect operation."""
    logger.debug("[%s] > %s > REDIRECT: Redirecting to %s", module, function, destination)

