"""Structured logging configuration for TomiLomos API.

This module sets up JSON-formatted structured logging across the application.
Sensitive fields (passwords, tokens, secrets) are filtered to prevent accidental logging.
"""

import json
import logging
import sys
from typing import Any, Dict, Mapping

from core.config import settings


class SensitiveDataFilter(logging.Filter):
    """Filter that redacts sensitive information from log records."""

    SENSITIVE_KEYS = {
        "password", "passwd", "pwd",
        "token", "jwt", "secret", "api_key", "apikey",
        "authorization", "auth", "bearer",
        "credential", "credentials",
        "access_token", "refresh_token",
        "database_url", "db_url", "db_password",
    }

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and redact sensitive data from log record."""
        if hasattr(record, "msg") and isinstance(record.msg, str):
            record.msg = self._redact_string(record.msg)
        
        if hasattr(record, "args") and isinstance(record.args, dict):
            record.args = self._redact_dict(record.args)
        
        return True

    @staticmethod
    def _redact_string(text: str) -> str:
        """Redact sensitive strings."""
        import re
        # Redact patterns with capturing group for key
        patterns_with_key = [
            r"(password|secret|token|api_key)[\s]*=[\s]*[^\s,}]+",
        ]
        for pattern in patterns_with_key:
            text = re.sub(pattern, r"\1=[REDACTED]", text, flags=re.IGNORECASE)
        
        # Redact patterns without capturing group
        patterns_no_key = [
            r"Bearer\s+[^\s]+",
            r"postgresql://[^\s]+",
        ]
        for pattern in patterns_no_key:
            text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
        
        return text

    @staticmethod
    def _redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive fields from dictionary."""
        redacted = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in SensitiveDataFilter.SENSITIVE_KEYS):
                redacted[key] = "[REDACTED]"
            elif isinstance(value, dict):
                redacted[key] = SensitiveDataFilter._redact_dict(value)
            else:
                redacted[key] = value
        return redacted


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Use __dict__ to safely access extra attributes
        if hasattr(record, '__dict__'):
            extra_keys = set(record.__dict__.keys()) - {
                'name', 'msg', 'args', 'created', 'filename', 'funcName', 'levelname',
                'levelno', 'lineno', 'module', 'msecs', 'message', 'pathname', 'process',
                'processName', 'relativeCreated', 'thread', 'threadName', 'exc_info',
                'exc_text', 'stack_info', 'asctime', 'getMessage',
            }
            for key in extra_keys:
                log_data[key] = getattr(record, key)

        return json.dumps(log_data)


def configure_logging() -> logging.Logger:
    """Configure structured logging for the application.
    
    Returns:
        logging.Logger: The root logger instance.
    """
    log_level = settings.log_level.upper()
    
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Add sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    console_handler.addFilter(sensitive_filter)
    
    # Set formatter
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    root_logger.addHandler(console_handler)
    
    return root_logger


# Initialize logger on module load
logger = configure_logging()
