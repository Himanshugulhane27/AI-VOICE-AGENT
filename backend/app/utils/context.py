"""Context variables for request-scoped data."""

from contextvars import ContextVar

# Stores the unique request ID for the current execution context.
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
