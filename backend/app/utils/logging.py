"""Structured logging configuration.

Configures the standard library ``logging`` module with a JSON-style
structured format suitable for production log aggregation systems
(e.g. Datadog, Stackdriver, ELK).
"""

import logging
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    """Emit log records as structured key=value lines.

    Produces deterministic, machine-parsable output while remaining
    human-readable in a terminal.  Each line contains:

    * ISO-8601 timestamp in UTC
    * Log level
    * Logger name
    * The log message
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a structured line."""
        from app.utils.context import request_id_ctx

        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()
        
        log_parts = [
            f"timestamp={timestamp}",
            f"level={record.levelname}",
            f"logger={record.name}",
        ]
        
        req_id = request_id_ctx.get("")
        if req_id:
            log_parts.append(f"request_id={req_id}")
            
        log_parts.append(f"message={record.getMessage()}")
        
        return " ".join(log_parts)


def setup_logging(level: str = "info") -> None:
    """Configure the root logger with structured output to stdout.

    Args:
        level: Logging level name (e.g. ``"info"``, ``"debug"``).
               Case-insensitive.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())

    root = logging.getLogger()
    root.setLevel(numeric_level)
    # Remove any pre-existing handlers to avoid duplicate output.
    root.handlers.clear()
    root.addHandler(handler)

    # Quiet noisy third-party loggers.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
