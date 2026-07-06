"""Health-check response schema."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response body for the ``GET /health`` endpoint."""

    status: str
    environment: str
    version: str
    timestamp: str
    google_sheets_status: str
    smtp_status: str
