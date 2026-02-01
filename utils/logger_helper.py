"""
Centralized logging helper to replace scattered print statements.

Provides consistent logging with module/function context for debugging
and production monitoring.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def log_entry(module: str, function: str, **kwargs) -> None:
    """
    Log function entry with optional context parameters.
    
    Args:
        module: Module name (e.g., 'auth', 'admin')
        function: Function name (e.g., 'login', 'register')
        **kwargs: Additional context to log
    """
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    message = f"[{module}] > {function} > ENTRY"
    if context:
        message += f": {context}"
    logger.info(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_query(module: str, function: str, description: str) -> None:
    """
    Log database query or data fetching operation.
    
    Args:
        module: Module name
        function: Function name
        description: Description of the query
    """
    message = f"[{module}] > {function} > QUERY: {description}"
    logger.debug(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_logic(module: str, function: str, decision: str) -> None:
    """
    Log business logic decision or conditional branch.
    
    Args:
        module: Module name
        function: Function name
        decision: Description of logic decision
    """
    message = f"[{module}] > {function} > LOGIC: {decision}"
    logger.debug(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_success(module: str, function: str, message_text: str) -> None:
    """
    Log successful operation completion.
    
    Args:
        module: Module name
        function: Function name
        message_text: Success message
    """
    message = f"[{module}] > {function} > SUCCESS: {message_text}"
    logger.info(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_error(module: str, function: str, error_message: str) -> None:
    """
    Log error or validation failure.
    
    Args:
        module: Module name
        function: Function name
        error_message: Error description
    """
    message = f"[{module}] > {function} > ERROR: {error_message}"
    logger.error(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_render(module: str, function: str, template: str) -> None:
    """
    Log template rendering operation.
    
    Args:
        module: Module name
        function: Function name
        template: Template filename
    """
    message = f"[{module}] > {function} > RENDER: Rendering {template}"
    logger.debug(message)
    print(f"[PROGRESSIVE LOG] {message}")


def log_redirect(module: str, function: str, destination: str) -> None:
    """
    Log HTTP redirect operation.
    
    Args:
        module: Module name
        function: Function name
        destination: Redirect destination
    """
    message = f"[{module}] > {function} > REDIRECT: Redirecting to {destination}"
    logger.debug(message)
    print(f"[PROGRESSIVE LOG] {message}")
